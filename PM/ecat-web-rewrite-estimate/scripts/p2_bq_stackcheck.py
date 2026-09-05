"""Verify three 'zero-use' features before reporting them as unused.

org_feature_usage_report derives create_my_list / create_customer_product_list /
create_maybe_list by discriminating create_stack on a `type` column. All three
came back as exactly zero orgs while create_stack itself reaches 130 orgs, which
means the discriminator is wrong, not that the features are unused. Confirm what
`type` actually contains.
"""
from bq import q

SRC = "`supercat-data-pipeline.WELD_RAW.mixpanel__events`"

print("--- create_stack: actual `type` values")
for r in q(f"""
    select coalesce(type, '<null>') as type, count(*) as n,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs
    from {SRC} where event_name = 'create_stack' group by 1 order by 2 desc
"""):
    print("   ", r)

print("\n--- which columns DO carry a stack discriminator?")
for r in q(f"""
    select coalesce(purpose, '<null>') as purpose,
           coalesce(context, '<null>') as context,
           count(*) as n
    from {SRC} where event_name = 'create_stack'
    group by 1, 2 order by 3 desc limit 12
"""):
    print("   ", r)

print("\n--- stack-family events overall")
for r in q(f"""
    select event_name, count(*) as n,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs
    from {SRC}
    where event_name in ('view_stack', 'view_smart_stack', 'edit_stack',
                         'email_stack', 'create_stack')
    group by 1 order by 3 desc
"""):
    print("   ", r)
