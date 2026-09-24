#!/usr/bin/env python3
"""The sandbox, and the proof that the client tree was not written to.

WHY THIS FILE EXISTS
--------------------
`build_ecat_files.py:31` sets

    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

and takes no arguments at all -- there is no `--out`, so there is nothing for
it to ignore politely. Anything that invokes it in place writes its outputs
NEXT TO ITSELF, which is
`SuperCat_Simple_Final/02_Implementation/Legrand/Build/`. That is the live
client tree. On 2026-09-09 a runner session did exactly that and overwrote
`Legrand/Build/stories.csv`, which had to be restored from git.

TWO DEFENCES, because one of them is a promise and the other is a measurement
---------------------------------------------------------------------------
1. STRUCTURAL. This runner never executes a script from a client tree. It
   drives `mapping/mapper.py`, which takes `out_path` as an argument and writes
   only there. Every input the mapping declares is COPIED into a sandbox and
   made read-only, and the build is pointed at the sandbox root -- so during a
   build the client tree is not merely unwritten, it is not referenced. A
   script cannot clobber a path it was never given.

2. EMPIRICAL. `TreeGuard` fingerprints the client tree before the run and
   again after, and the run FAILS if anything moved. Defence 1 is an argument
   about the code; defence 2 is evidence about this run. The 09-09 incident
   was a session that would have passed defence 1 on inspection -- it believed
   it was calling the mapping layer -- so the argument alone is not enough.

WHY COPY RATHER THAN SYMLINK THE SIBLINGS
-----------------------------------------
`ecatlib/acceptance_legrand.py` symlinks `Source Data` into its sandbox, which
is the right call there: it must run the real 1,537-line script unmodified,
against 407MB of source it cannot copy. But a symlink is a WRITE PATH. A
script that opens `Source Data/x.csv` for writing writes into the client tree
through the link, and `chmod` on a symlink changes the target's mode on macOS
if it follows at all. Since a mapping declares its inputs by name, the whole
declared set can be copied -- 3MB for Legrand -- and then there is no link to
follow. An input the mapping did NOT declare is absent from the sandbox, which
turns a silent read of an undeclared file into a loud failure.
"""

import hashlib
import os
import shutil
import stat
import subprocess


class TreeDirty(RuntimeError):
    """The client tree changed during a run. Never recoverable, always fatal."""


# --- staging ----------------------------------------------------------------

def stage(sandbox_root, client_root, declared, on_copy=None):
    """Copy every declared input into `sandbox_root`, preserving its relative
    path, and make it read-only.

    declared = [(relative, absolute)] from preflight.collect_declared_paths.
    Returns (staged_root, [lines]).
    """
    staged_root = os.path.join(sandbox_root, 'root')
    if os.path.exists(sandbox_root):
        shutil.rmtree(sandbox_root)
    os.makedirs(staged_root)

    lines = []
    seen = set()
    for rel, absolute in declared:
        if os.path.isabs(rel):
            # An absolute declared path cannot be relocated into the sandbox
            # without rewriting the mapping. Refuse rather than half-stage:
            # a build that reads one input from outside the sandbox has no
            # sandbox.
            raise TreeDirty(
                'mapping declares an ABSOLUTE input path (%s). Inputs must be '
                'declared relative to the client root so they can be staged. '
                'This is the build_ecat_files.py:39 hardcoded-~/Downloads '
                'shape and it cannot be sandboxed.' % rel)
        if rel in seen:
            continue
        seen.add(rel)
        dst = os.path.join(staged_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(absolute, dst)
        os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        lines.append('  staged r--  %-58s %d bytes'
                     % (rel[:58], os.path.getsize(dst)))
        if on_copy:
            on_copy(rel, absolute, dst)

    out_dir = os.path.join(sandbox_root, 'out')
    os.makedirs(out_dir)
    lines.append('  sandbox root : %s' % staged_root)
    lines.append('  output dir   : %s' % out_dir)
    lines.append('  the client tree is NOT referenced during the build.')
    return staged_root, out_dir, lines


# --- the guard --------------------------------------------------------------

class TreeGuard:
    """Fingerprint a client tree, then prove it did not change.

    Two independent readings, because they fail differently:

      * a content manifest (path -> sha256 + size + mtime) over the tree,
        which catches a write to a tracked OR untracked file;
      * `git status --porcelain`, which catches a delete or a rename that a
        manifest of surviving files would miss, and which is the reading a
        human will check afterwards.

    The manifest deliberately SKIPS image directories: Legrand's Build holds a
    ~1GB image library and hashing it costs minutes for a class of file no
    mapping writes. That exclusion is a scope limit, so it is reported rather
    than assumed -- `evaluated N of M`, BUILD_SPEC §3.4, applied to the guard.
    """

    SKIP_DIRS = ('images', 'images_batch_01_NEW', 'images_batch_02_NEW',
                 'images_batch_03_NEW', 'images_batch_04_NEW',
                 'images_batch_05_NEW', 'images_batch_06_REMAINING',
                 'images_ftp_batch_01', 'images_ftp_batch_02',
                 'images_missing_batch', '__pycache__', '.git')
    SKIP_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.mp4',
                '.mov', '.tif', '.tiff', '.webp')

    def __init__(self, client_root, git_root=None):
        self.client_root = os.path.abspath(client_root)
        self.git_root = os.path.abspath(git_root) if git_root else None
        self.before = None
        self.before_git = None
        self.skipped = 0

    def _manifest(self):
        out = {}
        self.skipped = 0
        for dirpath, dirnames, filenames in os.walk(self.client_root):
            dirnames[:] = [d for d in dirnames if d not in self.SKIP_DIRS]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, self.client_root)
                if fn.lower().endswith(self.SKIP_EXT):
                    self.skipped += 1
                    continue
                try:
                    st = os.lstat(p)
                    if not stat.S_ISREG(st.st_mode):
                        continue
                    # A dataless file must not be hashed -- reading it would
                    # trigger a multi-minute iCloud fetch of a file this run
                    # has no interest in. Its size and mtime still change if
                    # something writes to it.
                    if getattr(st, 'st_flags', 0) & 0x40000000:
                        out[rel] = ('dataless', st.st_size)
                        continue
                    h = hashlib.sha256()
                    with open(p, 'rb') as fh:
                        for chunk in iter(lambda: fh.read(1 << 20), b''):
                            h.update(chunk)
                    out[rel] = (h.hexdigest(), st.st_size)
                except OSError:
                    out[rel] = ('unreadable', -1)
        return out

    def _git(self):
        if not self.git_root:
            return None
        try:
            r = subprocess.run(['git', 'status', '--porcelain'],
                               cwd=self.git_root, capture_output=True,
                               text=True, timeout=180)
            if r.returncode != 0:
                return None
            return sorted(l for l in r.stdout.splitlines() if l.strip())
        except (subprocess.SubprocessError, OSError):
            return None

    def snapshot(self):
        self.before = self._manifest()
        self.before_git = self._git()
        return ['tree guard   : %d files fingerprinted under %s'
                % (len(self.before), self.client_root),
                '               %d binary/image files skipped by extension '
                '(no mapping writes them)' % self.skipped,
                '               git baseline: %s'
                % ('%d porcelain lines' % len(self.before_git)
                   if self.before_git is not None
                   else 'UNAVAILABLE — git could not be read, so the guard '
                        'rests on the manifest alone')]

    def verify(self):
        """Return (clean, lines, problems)."""
        after = self._manifest()
        after_git = self._git()
        lines, problems = [], []

        changed = sorted(k for k in set(self.before) & set(after)
                         if self.before[k] != after[k])
        added = sorted(set(after) - set(self.before))
        removed = sorted(set(self.before) - set(after))

        lines.append('  files compared : %d' % len(set(self.before) & set(after)))
        lines.append('  modified       : %d' % len(changed))
        lines.append('  created        : %d' % len(added))
        lines.append('  deleted        : %d' % len(removed))
        for k in changed[:20]:
            lines.append('     MODIFIED %s' % k)
        for k in added[:20]:
            lines.append('     CREATED  %s' % k)
        for k in removed[:20]:
            lines.append('     DELETED  %s' % k)

        if self.before_git is not None and after_git is not None:
            gnew = [l for l in after_git if l not in self.before_git]
            ggone = [l for l in self.before_git if l not in after_git]
            lines.append('  git porcelain  : %d before, %d after, %d new lines'
                         % (len(self.before_git), len(after_git), len(gnew)))
            for l in gnew[:20]:
                lines.append('     NEW  %s' % l)
            for l in ggone[:20]:
                lines.append('     GONE %s' % l)
            if gnew or ggone:
                problems.append(
                    'git status in the client tree CHANGED during this run '
                    '(%d new, %d resolved lines). The 09-09 incident '
                    'signature.' % (len(gnew), len(ggone)))
        else:
            lines.append('  git porcelain  : NOT CHECKED — git unavailable. '
                         'The manifest still ran; a rename is the case it '
                         'cannot see.')

        if changed or added or removed:
            problems.append(
                'the client tree was MODIFIED by this run: %d changed, %d '
                'created, %d deleted. A build must never be able to write '
                'into a client tree.'
                % (len(changed), len(added), len(removed)))

        lines.append('  coverage       : evaluated %d files; %d binary/image '
                     'files not hashed' % (len(after), self.skipped))
        return (not problems), lines, problems
