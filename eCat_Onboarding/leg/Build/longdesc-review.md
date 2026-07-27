# LongDesc / ShortDesc build review

**Fixed 2026-07-14:** the first pass copied the source `Product Name` straight into `LongDesc` verbatim. 668 of 1,020 rows (65%) exceeded eCat's 50-char limit (avg 61, max 143) — guaranteed length Warnings on import and mid-word truncation in the app's grid/list/order views. `ShortDesc` was also left blank on all 1,020 rows, so there was no shorter fallback name either.

## What the build now does

1. Strip `®`/`™` and the leading brand word (redundant with `CollectionCodes` — adorne/radiant is already shown as the Collection).
2. Strip the trailing ", with Microban" marketing suffix (antimicrobial protection is a line-wide feature on nearly every SKU, not a differentiator — not worth the character budget in the display name).
3. Locate the SKU's `Finish` value inside what's left (hyphen/space insensitive) and anchor it to the end, so truncation trims the *description*, never the finish/color word that differentiates finish-variant SKUs from each other in a list view.
4. If still over 50 chars, truncate at the last word boundary (never mid-word) and log it below for a human spot-check.
5. `ShortDesc` is the cleaned name truncated to 15 chars at a word boundary — best-effort; still far better than blank for narrow admin/order-form columns.

**Result: 0 of 1020 rows exceed 50 chars.** 386 rows needed word-boundary truncation to fit — listed below for a quick human read-through (most reasonable; a few may read better with manual editorial polish).

## Rows that required truncation (386)

| BaseItemCode | Original Product Name | Built LongDesc |
|---|---|---|
| ADSM703HG2 | adorne® 700W Incandescent/Halogen Motion Sensor Dimmer, Graphite, with Microban® | 700W Incandescent/Halogen Motion, Graphite |
| ADSM703HM2 | adorne® 700W Incandescent/Halogen Motion Sensor Dimmer, Magnesium, with Microban® | 700W Incandescent/Halogen Motion, Magnesium |
| ADSM703HW2 | adorne® 700W Incandescent/Halogen Motion Sensor Dimmer, White, with Microban® | 700W Incandescent/Halogen Motion Sensor, White |
| ASVS12M4 | adorne® Motion Sensor Switch, Manual On/Auto Off, Magnesium, with Microban® | Motion Sensor Switch, Manual On/Auto, Magnesium |
| AGFTR2152G4 | adorne® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, Graphite | Tamper-Resistant 15A Duplex Self-Test, Graphite |
| AGFTR2152M4 | adorne® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, Magnesium | Tamper-Resistant 15A Duplex Self-Test, Magnesium |
| AGFTR2152W4 | adorne® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, White | Tamper-Resistant 15A Duplex Self-Test, White |
| AGFTR2153G4 | adorne® Plus Size Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, Graphite | Plus Size Tamper-Resistant 15A Duplex, Graphite |
| AGFTR2153M4 | adorne® Plus Size Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, Magnesium | Plus Size Tamper-Resistant 15A Duplex, Magnesium |
| AGFTR2153W4 | adorne® Plus Size Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles, White | Plus Size Tamper-Resistant 15A Duplex Self-, White |
| AGFTR2202G4 | adorne® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles, Graphite | Tamper-Resistant 20A Duplex Self-Test, Graphite |
| AGFTR2202M4 | adorne® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles, Magnesium | Tamper-Resistant 20A Duplex Self-Test, Magnesium |
| AGFTR2202W4 | adorne® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles, White | Tamper-Resistant 20A Duplex Self-Test, White |
| ARCD152G10 | adorne® 15A Tamper-Resistant Dual-Controlled Outlet, Graphite | 15A Tamper-Resistant Dual-Controlled, Graphite |
| ARCD152M10 | adorne® 15A Tamper-Resistant Dual-Controlled Outlet, Magnesium | 15A Tamper-Resistant Dual-Controlled, Magnesium |
| ARCD202M10 | adorne® 20A Tamper-Resistant Dual-Controlled Outlet, Magnesium | 20A Tamper-Resistant Dual-Controlled, Magnesium |
| ARCH152G10 | adorne® 15A Tamper-Resistant Half-Controlled Outlet, Graphite | 15A Tamper-Resistant Half-Controlled, Graphite |
| ARCH152M10 | adorne® 15A Tamper-Resistant Half-Controlled Outlet, Magnesium | 15A Tamper-Resistant Half-Controlled, Magnesium |
| ARTR153G4 | adorne® 15A Dual Tamper-Resistant Plus-Size Outlet, Graphite | 15A Dual Tamper-Resistant Plus-Size, Graphite |
| ARTR153M4 | adorne® 15A Dual Tamper-Resistant Plus-Size Outlet,Magnesium | 15A Dual Tamper-Resistant Plus-Size, Magnesium |
| ARTRUSB153M4WP | adorne® Dual-USB Outlet with Magnesium Wall Plate, Magnesium | Dual-USB Outlet with Wall Plate, Magnesium |
| ARTRUSB153W4WP | adorne® Dual-USB Outlet with Gloss White Wall Plate, White | Dual-USB Outlet with Gloss Wall Plate, White |
| ARTRUSB156ACG4 | adorne® 15A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, Graphite | 15A Tamper-Resistant Ultra-Fast USB, Graphite |
| ARTRUSB156ACM4 | adorne® 15A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, Magnesium | 15A Tamper-Resistant Ultra-Fast USB, Magnesium |
| ARTRUSB156ACW4 | adorne® 15A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, White | 15A Tamper-Resistant Ultra-Fast USB Type-, White |
| ARTRUSB206ACG4 | adorne® 20A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, Graphite | 20A Tamper-Resistant Ultra-Fast USB, Graphite |
| ARTRUSB206ACM4 | adorne® 20A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, Magnesium | 20A Tamper-Resistant Ultra-Fast USB, Magnesium |
| ARTRUSB206ACW4 | adorne® 20A Tamper-Resistant Ultra-Fast USB Type-A/C Outlet, White | 20A Tamper-Resistant Ultra-Fast USB Type-, White |
| ARUSB30PDM4 | adorne® Ultra-Fast Plus Power Delivery USB Type-C/C Outlet Module, Magnesium | Ultra-Fast Plus Power Delivery USB, Magnesium |
| ARUSB30PDW4 | adorne® Ultra-Fast Plus Power Delivery USB Type-C/C Outlet Module, White | Ultra-Fast Plus Power Delivery USB Type-, White |
| ARUSB30PDG4 | adorne® Ultra-Fast Plus Power Delivery USB Type-C/C Outlet Module, Graphite | Ultra-Fast Plus Power Delivery USB Type-, Graphite |
| ARTRUSB15PD30M4 | adorne® 15A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, Magnesium | 15A Tamper-Resistant Ultra-Fast Plus, Magnesium |
| ARTRUSB15PD30W4 | adorne® 15A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, White | 15A Tamper-Resistant Ultra-Fast Plus, White |
| ARTRUSB15PD30G4 | adorne® 15A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, Graphite | 15A Tamper-Resistant Ultra-Fast Plus, Graphite |
| ARTRUSB20PD30M4 | adorne® 20A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, Magnesium | 20A Tamper-Resistant Ultra-Fast Plus, Magnesium |
| ARTRUSB20PD30W4 | adorne® 20A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, White | 20A Tamper-Resistant Ultra-Fast Plus, White |
| ARTRUSB20PD30G4 | adorne® 20A Tamper-Resistant Ultra-Fast Plus Power Delivery USB Type-C/C Outlet, Plus-Size, Graphite | 20A Tamper-Resistant Ultra-Fast Plus, Graphite |
| AWC1G2BBN4 | adorne® Brushed Black Nickel One-Gang Screwless Wall Plate | One-Gang Screwless Wall, Brushed Black Nickel |
| AWC3GBBN4 | adorne® Brushed Black Nickel Three-Gang Screwless Wall Plate | Three-Gang Screwless Wall, Brushed Black Nickel |
| AWC1G3BSB4 | adorne® Brushed Satin Brass One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless, Brushed Satin Brass |
| AWC3GBSB4 | adorne® Brushed Satin Brass Three-Gang Screwless Wall Plate | Three-Gang Screwless Wall, Brushed Satin Brass |
| AWC4GBSB4 | adorne® Brushed Satin Brass Four-Gang Screwless Wall Plate | Four-Gang Screwless Wall, Brushed Satin Brass |
| AWC1G3BS4 | adorne® Brushed Stainless Steel One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless, Brushed Stainless Steel |
| AWC1G2BS4 | adorne® Brushed Stainless Steel One-Gang Screwless Wall Plate | One-Gang Screwless Wall, Brushed Stainless Steel |
| AWC2GBS4 | adorne® Brushed Stainless Steel Two-Gang Screwless Wall Plate | Two-Gang Screwless Wall, Brushed Stainless Steel |
| AWC3GBS4 | adorne® Brushed Stainless Steel Three-Gang Screwless Wall Plate | Three-Gang Screwless, Brushed Stainless Steel |
| AWC4GBS4 | adorne® Brushed Stainless Steel Four-Gang Screwless Wall Plate | Four-Gang Screwless, Brushed Stainless Steel |
| AWC1G2MAC4 | adorne® Matte Antique Copper One-Gang Screwless Wall Plate | One-Gang Screwless Wall, Matte Antique Copper |
| AWC1G3MAC4 | adorne® Matte Antique Copper One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless, Matte Antique Copper |
| AWC2GMAC4 | adorne® Matte Antique Copper Two-Gang Screwless Wall Plate | Two-Gang Screwless Wall, Matte Antique Copper |
| AWC3GMAC4 | adorne® Matte Antique Copper Three-Gang Screwless Wall Plate | Three-Gang Screwless Wall, Matte Antique Copper |
| AWC4GMAC4 | adorne® Matte Antique Copper Four-Gang Screwless Wall Plate | Four-Gang Screwless Wall, Matte Antique Copper |
| AWC1G3OB4 | adorne® Oil-Rubbed Bronze One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless Wall, Oil-Rubbed Bronze |
| AWM1G3BLS4 | adorne® Black Stainless One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless Wall, Black Stainless |
| AWM1G3MS4 | adorne® Brushed Stainless One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless Wall, Brushed Stainless |
| AWM1G3M4 | adorne® Custom One-Gang-Plus Screwless Wall Plate, Magnesium Trim | Custom One-Gang-Plus Screwless Wall, Magnesium |
| AWM1G2M4 | adorne® Custom One-Gang Screwless Wall Plate, Magnesium Trim | Custom One-Gang Screwless Wall Plate, Magnesium |
| AWM2GM4 | adorne® Custom Two-Gang Screwless Wall Plate, Magnesium Trim | Custom Two-Gang Screwless Wall Plate, Magnesium |
| AWM3GM4 | adorne® Custom Three-Gang Screwless Wall Plate, Magnesium Trim | Custom Three-Gang Screwless Wall, Magnesium |
| AWM4GM4 | adorne® Custom Four-Gang Screwless Wall Plate, Magnesium Trim | Custom Four-Gang Screwless Wall, Magnesium |
| AWM1G3MWW4 | adorne® Mirror White-on-White One-Gang+ Screwless Wall Plate | on-White One-Gang+ Screwless Wall, Mirror White |
| AWM1G2MWW4 | adorne® Mirror White-on-White One-Gang Screwless Wall Plate | on-White One-Gang Screwless Wall, Mirror White |
| AWM3GMWW4 | adorne® Mirror White-on-White Three-Gang Screwless Wall Plate | on-White Three-Gang Screwless Wall, Mirror White |
| AWM4GMWW4 | adorne® Mirror White-on-White Four-Gang Screwless Wall Plate | on-White Four-Gang Screwless Wall, Mirror White |
| AWM1G3SP4 | adorne® Spiraled Stainless One-Gang-Plus Screwless Wall Plate | One-Gang-Plus Screwless Wall, Spiraled Stainless |
| AWM3GSP4 | adorne® Spiraled Stainless Three-Gang Screwless Wall Plate | Three-Gang Screwless Wall, Spiraled Stainless |
| AWM1G3W4 | adorne® Custom One-Gang-Plus Screwless Wall Plate, White Trim | Custom One-Gang-Plus Screwless Wall, White |
| AWM3GW4 | adorne® Custom Three-Gang Screwless Wall Plate, White Trim | Custom Three-Gang Screwless Wall Plate, White |
| AWP1G3WHW4 | adorne® Gloss White-on-White One-Gang-Plus Screwless Wall Plate with Microban® | One-Gang-Plus Screwless, Gloss White-on-White |
| AWP1G2WHW10 | adorne® Gloss White-on-White One-Gang Screwless Wall Plate with Microban® | One-Gang Screwless Wall, Gloss White-on-White |
| AWP2GWHW10 | adorne® Gloss White-on-White Two-Gang Screwless Wall Plate with Microban® | Two-Gang Screwless Wall, Gloss White-on-White |
| AWP3GWHW4 | adorne® Gloss White-on-White Three-Gang Screwless Wall Plate with Microban® | Three-Gang Screwless Wall, Gloss White-on-White |
| AWP4GWHW4 | adorne® Gloss White-on-White Four-Gang Screwless Wall Plate with Microban® | Four-Gang Screwless Wall, Gloss White-on-White |
| AWP5GWHW1 | adorne® Gloss White-on-White Five-Gang Screwless Wall Plate with Microban® | Five-Gang Screwless Wall, Gloss White-on-White |
| AWP6GWHW1 | adorne® Gloss White-on-White Six-Gang Screwless Wall Plate with Microban® | Six-Gang Screwless Wall, Gloss White-on-White |
| WNAR203M1 | adorne® 20A Smart Outlet with Netatmo, Plus-Size, Magnesium | 20A Smart Outlet with Netatmo, Plus-, Magnesium |
| WNAL63CKITG1 | adorne® Remote Smart Dimmer with Netatmo Color Change Kit, Graphite | Remote Smart Dimmer with Netatmo Color, Graphite |
| WNAL63CKITM1 | adorne® Remote Smart Dimmer with Netatmo Color Change Kit, Magnesium | Remote Smart Dimmer with Netatmo, Magnesium |
| WNAL63CKITW1 | adorne® Remote Smart Dimmer with Netatmo Color Change Kit, White | Remote Smart Dimmer with Netatmo Color, White |
| WNAL23CKITG1 | adorne® Remote Smart Switch with Netatmo Color Change Kit, Graphite | Remote Smart Switch with Netatmo Color, Graphite |
| WNAL23CKITM1 | adorne® Remote Smart Switch with Netatmo Color Change Kit, Magnesium | Remote Smart Switch with Netatmo, Magnesium |
| WNAL23CKITW1 | adorne® Remote Smart Switch with Netatmo Color Change Kit, White | Remote Smart Switch with Netatmo Color, White |
| WNAL33CKITG1 | adorne® Smart Home/Away Switch with Netatmo Color Change Kit, Graphite | Smart Home/Away Switch with Netatmo, Graphite |
| WNAL33CKITM1 | adorne® Smart Home/Away Switch with Netatmo Color Change Kit, Magnesium | Smart Home/Away Switch with Netatmo, Magnesium |
| WNAL33CKITW1 | adorne® Smart Home/Away Switch with Netatmo Color Change Kit, White | Smart Home/Away Switch with Netatmo Color, White |
| WNACB40CKITG1 | adorne® Smart Scene Controller with Netatmo Color Change Kit, Graphite | Smart Scene Controller with Netatmo, Graphite |
| WNACB40CKITM1 | adorne® Smart Scene Controller with Netatmo Color Change Kit, Magnesium | Smart Scene Controller with Netatmo, Magnesium |
| WNACB40CKITW1 | adorne® Smart Scene Controller with Netatmo Color Change Kit, White | Smart Scene Controller with Netatmo Color, White |
| WNAH2M1 | adorne® Smart Surface-Mount Gateway with Netatmo, Magnesium | Smart Surface-Mount Gateway with, Magnesium |
| WNAL10CKITG1 | adorne® Smart Switch with Netatmo Color Change Kit, Graphite | Smart Switch with Netatmo Color Change, Graphite |
| WNAL10CKITM1 | adorne® Smart Switch with Netatmo Color Change Kit, Magnesium | Smart Switch with Netatmo Color, Magnesium |
| WNAL43CKITG1 | adorne® Smart Wake/Sleep Switch with Netatmo Color Change Kit, Graphite | Smart Wake/Sleep Switch with Netatmo, Graphite |
| WNAL43CKITM1 | adorne® Smart Wake/Sleep Switch with Netatmo Color Change Kit, Magnesium | Smart Wake/Sleep Switch with Netatmo, Magnesium |
| WNAL43CKITW1 | adorne® Smart Wake/Sleep Switch with Netatmo Color Change Kit, White | Smart Wake/Sleep Switch with Netatmo, White |
| WNAL33M1 | adorne® Wireless Home/Away Smart Switch with Netatmo, Magnesium | Wireless Home/Away Smart Switch with, Magnesium |
| WNAL33G1 | adorne® Wireless Home/Away Smart Switch with Netatmo, Graphite | Wireless Home/Away Smart Switch with, Graphite |
| WNAL33W1 | adorne® Wireless Home/Away Smart Switch with Netatmo, White | Wireless Home/Away Smart Switch with, White |
| WNAL63M1 | adorne® Wireless Remote Smart Dimmer with Netatmo, Magnesium | Wireless Remote Smart Dimmer with, Magnesium |
| WNAL63G1 | adorne® Wireless Remote Smart Dimmer with Netatmo, Graphite | Wireless Remote Smart Dimmer with, Graphite |
| WNAL23G1 | adorne® Wireless Remote Smart Switch with Netatmo, Graphite | Wireless Remote Smart Switch with, Graphite |
| WNAL23M1 | adorne® Wireless Remote Smart Switch with Netatmo, Magnesium | Wireless Remote Smart Switch with, Magnesium |
| WNACB40M1 | adorne® Wireless Smart Scene Controller with Netatmo, Magnesium | Wireless Smart Scene Controller with, Magnesium |
| WNACB40G1 | adorne® Wireless Smart Scene Controller with Netatmo, Graphite | Wireless Smart Scene Controller with, Graphite |
| WNACB40W1 | adorne® Wireless Smart Scene Controller with Netatmo, White | Wireless Smart Scene Controller with, White |
| WNAL43M1 | adorne® Wireless Wake/Sleep Smart Switch with Netatmo, Magnesium | Wireless Wake/Sleep Smart Switch with, Magnesium |
| WNAL43G1 | adorne® Wireless Wake/Sleep Smart Switch with Netatmo, Graphite | Wireless Wake/Sleep Smart Switch with, Graphite |
| WNAL43W1 | adorne® Wireless Wake/Sleep Smart Switch with Netatmo, White | Wireless Wake/Sleep Smart Switch with, White |
| RCD38TRBK | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Black | Single Pole/3-Way Switch with 15A Tamper-, Black |
| RCD38TRDBCC6 | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Dark Bronze | Single Pole/3-Way Switch with 15A, Dark Bronze |
| RCD38TRGRY | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Gray | Single Pole/3-Way Switch with 15A Tamper-, Gray |
| RCD38TRI | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Ivory | Single Pole/3-Way Switch with 15A Tamper-, Ivory |
| RCD38TRLA | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Light Almond | Single Pole/3-Way Switch with 15A, Light Almond |
| RCD38TRNICC6 | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, Nickel | Single Pole/3-Way Switch with 15A Tamper-, Nickel |
| RCD38TRW | radiant® Single Pole/3-Way Switch with 15A Tamper-Resistant Outlet, White | Single Pole/3-Way Switch with 15A Tamper-, White |
| RCD38TR | radiant® Single-Pole/3-Way Switch with 15A Tamper-Resistant Outlet | Single-Pole/3-Way Switch with 15A Tamper- |
| RCD113 | radiant® Two Single-Pole Switches & Single Pole/3-Way Switch | Two Single-Pole Switches & Single Pole/3-Way |
| RCD113BK | radiant® Two Single-Pole Switches and Single Pole/3-Way Switch, Black | Two Single-Pole Switches and Single Pole/3-, Black |
| RCD113GRY | radiant® Two Single-Pole Switches and Single Pole/3-Way Switch, Gray | Two Single-Pole Switches and Single Pole/3-, Gray |
| RCD113I | radiant® Two Single-Pole Switches and Single Pole/3-Way Switch, Ivory | Two Single-Pole Switches and Single Pole/3-, Ivory |
| RCD113LA | radiant® Two Single-Pole Switches and Single Pole/3-Way Switch, Light Almond | Two Single-Pole Switches and, Light Almond |
| RCD113W | radiant® Two Single-Pole Switches and Single Pole/3-Way Switch, White | Two Single-Pole Switches and Single Pole/3-, White |
| HMKITBK | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Black | Interchangeable Face Cover for Multi-, Black |
| HMKIT | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Brown | Interchangeable Face Cover for Multi-, Brown |
| HMKITDB | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Dark Bronze | Interchangeable Face Cover for Multi-, Dark Bronze |
| HMKITGRY | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Gray | Interchangeable Face Cover for Multi-, Gray |
| HMKITI | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Ivory | Interchangeable Face Cover for Multi-, Ivory |
| HMKITLA | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Light Almond | Interchangeable Face Cover for, Light Almond |
| HMKITNI | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, Nickel | Interchangeable Face Cover for Multi-, Nickel |
| HMKITW | radiant® Interchangeable Face Cover for Multi-Location Master Dimmer, White | Interchangeable Face Cover for Multi-, White |
| 1597SWTTRBKCCD4 | radiant® Combination Single Pole Switch and Tamper-Reistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Black | Combination Single Pole Switch and Tamper-, Black |
| 1597SWTTRICCD4 | radiant® Combination Single Pole Switch and Tamper-Reistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Ivory CC | Combination Single Pole Switch and Tamper-, Ivory |
| 1597SWTTRLACCD4 | radiant® Combination Single Pole Switch and Tamper-Reistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Light Almond CC | Combination Single Pole Switch and, Light Almond |
| 1597SWTTRWCCD4 | radiant® Combination Single Pole Switch and Tamper-Reistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White CC | Combination Single Pole Switch and Tamper-, White |
| 1597TRA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with Audible Alarm and SafeLock® Protection, Brown | Tamper-Resistant 15A Duplex Self-Test, Brown |
| 1597TRAI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with Audible Alarm and SafeLock® Protection, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597TRALA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with Audible Alarm and SafeLock® Protection, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597TRAW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with Audible Alarm and SafeLock® Protection, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597NTLTRDBCC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Dark Bronze | Tamper-Resistant 15A Duplex Self-, Dark Bronze |
| 1597NTLTRI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597NTLTRLA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597NTLTRNICC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Nickel CC | Tamper-Resistant 15A Duplex Self-Test GFCI |
| 1597NTLTRW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597TRBK | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Black | Tamper-Resistant 15A Duplex Self-Test, Black |
| 1597TR | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Brown | Tamper-Resistant 15A Duplex Self-Test, Brown |
| 1597TRDBCC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Dark Bronze CC | Tamper-Resistant 15A Duplex Self-, Dark Bronze |
| 1597TRGCC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Graphite CC | Tamper-Resistant 15A Duplex Self-Test, Graphite |
| 1597TRGRY | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Gray | Tamper-Resistant 15A Duplex Self-Test GFCI, Gray |
| 1597TRI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597TRLA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597TRNICC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Nickel CC | Tamper-Resistant 15A Duplex Self-Test, Nickel |
| 1597TRW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597TRSGLBK | radiant® Tamper-Resistant 15A Simplex Self-Test GFCI Receptacles with SafeLock® Protection, Black | Tamper-Resistant 15A Simplex Self-Test, Black |
| 1597TRSGL | radiant® Tamper-Resistant 15A Simplex Self-Test GFCI Receptacles with SafeLock® Protection, Brown | Tamper-Resistant 15A Simplex Self-Test, Brown |
| 1597TRSGLI | radiant® Tamper-Resistant 15A Simplex Self-Test GFCI Receptacles with SafeLock® Protection, Ivory | Tamper-Resistant 15A Simplex Self-Test, Ivory |
| 2097TRBK | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Black | Tamper-Resistant 20A Duplex Self-Test, Black |
| 2097TR | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Brown | Tamper-Resistant 20A Duplex Self-Test, Brown |
| 2097TRDBCC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Dark Bronze CC | Tamper-Resistant 20A Duplex Self-, Dark Bronze |
| 2097TRGCC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Graphite CC | Tamper-Resistant 20A Duplex Self-Test, Graphite |
| 2097TRGRY | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Gray | Tamper-Resistant 20A Duplex Self-Test GFCI, Gray |
| 2097TRI | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Ivory | Tamper-Resistant 20A Duplex Self-Test, Ivory |
| 2097TRLA | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Light Almond | Tamper-Resistant 20A Duplex Self-, Light Almond |
| 2097TRNICC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Nickel CC | Tamper-Resistant 20A Duplex Self-Test, Nickel |
| 2097TRRED | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, Red | Tamper-Resistant 20A Duplex Self-Test GFCI, Red |
| 2097TRW | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacle with SafeLock® Protection, White | Tamper-Resistant 20A Duplex Self-Test, White |
| 2097NTLTRGRY | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Gray | Tamper-Resistant 20A Duplex Self-Test GFCI, Gray |
| 2097NTLTRI | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Ivory | Tamper-Resistant 20A Duplex Self-Test, Ivory |
| 2097NTLTRLA | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, Light Almond | Tamper-Resistant 20A Duplex Self-, Light Almond |
| 2097NTLTRW | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection and Night Light, White | Tamper-Resistant 20A Duplex Self-Test, White |
| 1597TRAPLW | radiant® Tamper-Resistant Sensitive Appliance 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White | Tamper-Resistant Sensitive Appliance 15A, White |
| 2097TRAPLW | radiant® Tamper-Resistant Sensitive Appliance Duplex 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White | Tamper-Resistant Sensitive Appliance, White |
| 1597TRWRBK | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Black | Tamper-Resistant Weather-Resistant 15A, Black |
| 1597TRWR | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Brown | Tamper-Resistant Weather-Resistant 15A, Brown |
| 1597TRWRGRY | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Gray | Tamper-Resistant Weather-Resistant 15A, Gray |
| 1597TRWRI | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Ivory | Tamper-Resistant Weather-Resistant 15A, Ivory |
| 1597TRWRLA | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Light Almond | Tamper-Resistant Weather-Resistant, Light Almond |
| 1597TRWRW | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White | Tamper-Resistant Weather-Resistant 15A, White |
| 2097TRWRBK | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Black | Tamper-Resistant Weather-Resistant 20A, Black |
| 2097TRWR | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Brown | Tamper-Resistant Weather-Resistant 20A, Brown |
| 2097TRWRGRY | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Gray | Tamper-Resistant Weather-Resistant 20A, Gray |
| 2097TRWRI | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Ivory | Tamper-Resistant Weather-Resistant 20A, Ivory |
| 2097TRWRLA | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Light Almond | Tamper-Resistant Weather-Resistant, Light Almond |
| 2097TRWRW | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, White | Tamper-Resistant Weather-Resistant 20A, White |
| 1597TRUSBAA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Brown | Tamper-Resistant 15A Duplex Self-Test, Brown |
| 1597TRUSBAABK | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Black | Tamper-Resistant 15A Duplex Self-Test, Black |
| 1597TRUSBAAGC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Graphite C4 | Tamper-Resistant 15A Duplex Self-Test, Graphite |
| 1597TRUSBAAGRY | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Gray | Tamper-Resistant 15A Duplex Self-Test GFCI, Gray |
| 1597TRUSBAAI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597TRUSBAALA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597TRUSBAANIC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, Nickel C4 | Tamper-Resistant 15A Duplex Self-Test, Nickel |
| 1597TRUSBAAW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/A, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597TRUSBAC | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Brown | Tamper-Resistant 15A Duplex Self-Test, Brown |
| 1597TRUSBACBK | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Black | Tamper-Resistant 15A Duplex Self-Test, Black |
| 1597TRUSBACDBC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Dark Bronze C4 | Tamper-Resistant 15A Duplex Self-, Dark Bronze |
| 1597TRUSBACGC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Graphite C4 | Tamper-Resistant 15A Duplex Self-Test, Graphite |
| 1597TRUSBACGRY | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Gray | Tamper-Resistant 15A Duplex Self-Test GFCI, Gray |
| 1597TRUSBACI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597TRUSBACLA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597TRUSBACNIC4 | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C, Nickel C4 | Tamper-Resistant 15A Duplex Self-Test, Nickel |
| 1597TRUSBACW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597TRUSBCCI | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type C/C Outlet, Ivory | Tamper-Resistant 15A Duplex Self-Test, Ivory |
| 1597TRUSBCCLA | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type C/C Outlet, Light Almond | Tamper-Resistant 15A Duplex Self-, Light Almond |
| 1597TRUSBCCW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type C/C, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 1597TRWRUSBACBK | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C Outlets, Black | Tamper-Resistant Weather-Resistant 15A, Black |
| 1597TRWRUSBACGRY | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C Outlets, Gray | Tamper-Resistant Weather-Resistant 15A, Gray |
| 1597TRWRUSBACI | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C Outlets, Ivory | Tamper-Resistant Weather-Resistant 15A, Ivory |
| 1597TRWRUSBACLA | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C Outlets, Light Almond | Tamper-Resistant Weather-Resistant, Light Almond |
| 1597TRWRUSBACW | radiant® Tamper-Resistant Weather-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type A/C Outlets, White | Tamper-Resistant Weather-Resistant 15A, White |
| 1597TRWRUSBCCBK | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type C/C, Black | Tamper-Resistant 15A Duplex Self-Test, Black |
| 1597TRWRUSBCCW | radiant® Tamper-Resistant 15A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, USB Type C/C, White | Tamper-Resistant 15A Duplex Self-Test, White |
| 2097TRUSBAA | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Brown | Tamper-Resistant 20A Duplex Self-Test, Brown |
| 2097TRUSBAABK | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Black | Tamper-Resistant 20A Duplex Self-Test, Black |
| 2097TRUSBAAGRY | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Gray | Tamper-Resistant 20A Duplex Self-Test GFCI, Gray |
| 2097TRUSBAAI | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Ivory | Tamper-Resistant 20A Duplex Self-Test, Ivory |
| 2097TRUSBAALA | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Light Almond | Tamper-Resistant 20A Duplex Self-, Light Almond |
| 2097TRUSBAARED | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, Red | Tamper-Resistant 20A Duplex Self-Test GFCI, Red |
| 2097TRUSBAAW | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/A Outlet, White | Tamper-Resistant 20A Duplex Self-Test, White |
| 2097TRUSBAC | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Brown | Tamper-Resistant 20A Duplex Self-Test, Brown |
| 2097TRUSBACBK | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Black | Tamper-Resistant 20A Duplex Self-Test, Black |
| 2097TRUSBACDBC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Dark Bronze | Tamper-Resistant 20A Duplex Self-, Dark Bronze |
| 2097TRUSBACGC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Graphite | Tamper-Resistant 20A Duplex Self-Test, Graphite |
| 2097TRUSBACGRY | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Gray | Tamper-Resistant 20A Duplex Self-Test GFCI, Gray |
| 2097TRUSBACI | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Ivory | Tamper-Resistant 20A Duplex Self-Test, Ivory |
| 2097TRUSBACLA | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Light Almond | Tamper-Resistant 20A Duplex Self-, Light Almond |
| 2097TRUSBACNIC4 | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Nickel | Tamper-Resistant 20A Duplex Self-Test, Nickel |
| 2097TRUSBACRED | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Red | Tamper-Resistant 20A Duplex Self-Test GFCI, Red |
| 2097TRUSBACW | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, White | Tamper-Resistant 20A Duplex Self-Test, White |
| 2097TRUSBCCW | radiant® Tamper-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type C/C Outlet, White | Tamper-Resistant 20A Duplex Self-Test, White |
| 2097TRWRUSBACBK | radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI Receptacles with SafeLock® Protection, Type A/C Outlet, Black | Tamper-Resistant Weather-Resistant 20A, Black |
| 2097TRWRUSBACGRY | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type A/C Outlet, Gray | Tamper-Resistant Weather-Resistant Duplex, Gray |
| 2097TRWRUSBACI | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type A/C Outlet, Ivory | Tamper-Resistant Weather-Resistant Duplex, Ivory |
| 2097TRWRUSBACLA | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type A/C Outlet, Light Almond | Tamper-Resistant Weather-Resistant, Light Almond |
| 2097TRWRUSBACW | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type A/C Outlet, White | Tamper-Resistant Weather-Resistant Duplex, White |
| 2097TRWRUSBCCBK | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type A/C Outlet, Black | Tamper-Resistant Weather-Resistant Duplex, Black |
| 2097TRWRUSBCCW | radiant® Tamper-Resistant Weather-Resistant Duplex Self-Test GFCI with USB Type C/C Outlet, White | Tamper-Resistant Weather-Resistant Duplex, White |
| RHLV1103PTC | radiant® 120V, 1100VA Magnetic Low-Voltage Single Pole/3-Way Dimmer, Tri-Color | 120V, 1100VA Magnetic Low-Voltage Single Pole/3- |
| RHLV1103PW | radiant® 120V, 1100VA Magnetic Low-Voltage Single Pole/3-Way Dimmer, White | 120V, 1100VA Magnetic Low-Voltage Single, White |
| RHLV703PTC | radiant® 120V, 700VA, Magnetic Low-Voltage Single Pole/3-Way Dimmer, Tri-Color | 120V, 700VA, Magnetic Low-Voltage Single Pole/3- |
| RHLV703PW | radiant® 120V, 700VA, Magnetic Low-Voltage Single Pole/3-Way Dimmer, White | 120V, 700VA, Magnetic Low-Voltage Single, White |
| RW600UTC | radiant® 600W 120V Single Pole Occupancy and Vacancy Sensor, Tri-Color | 600W 120V Single Pole Occupancy and, Tri-Color |
| RHDH163PBCCCV4 | radiant® Fan Speed Control Switch and De-Hummer, Single-Pole/3-Way, Bi-Color | Fan Speed Control Switch and De-, Bi-Color |
| HMRKITBK | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Black | Interchangeable Face Cover for Multi-, Black |
| HMRKIT | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Brown | Interchangeable Face Cover for Multi-, Brown |
| HMRKITDB | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Dark Bronze | Interchangeable Face Cover for Multi-, Dark Bronze |
| HMRKITGRY | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Gray | Interchangeable Face Cover for Multi-, Gray |
| HMRKITI | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Ivory | Interchangeable Face Cover for Multi-, Ivory |
| HMRKITLA | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Light Almond | Interchangeable Face Cover for, Light Almond |
| HMRKITNI | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, Nickel | Interchangeable Face Cover for Multi-, Nickel |
| HMRKITW | radiant® Interchangeable Face Cover for Multi-Location Remote Dimmer, White | Interchangeable Face Cover for Multi-, White |
| RHL153PWPW | radiant® LED Advanced 150W Single Pole/3-Way Dimmer with Wall Plate, White | LED Advanced 150W Single Pole/3-Way, White |
| RHL153PDB | radiant® LED Advanced 150W Single Pole/3-Way Dimmer, Dark Bronze | LED Advanced 150W Single Pole/3-Way, Dark Bronze |
| RHL153PG | radiant® LED Advanced 150W Single Pole/3-Way Dimmer, Graphite | LED Advanced 150W Single Pole/3-Way, Graphite |
| RHL153PLA | radiant® LED Advanced 150W Single Pole/3-Way Dimmer, Light Almond | LED Advanced 150W Single Pole/3-, Light Almond |
| RHL153PW10PK | radiant® LED Advanced 150W Single Pole/3-Way Dimmer, White, 10-Pack | LED Advanced 150W Single Pole/3-Way, White |
| WNRL33LA | radiant® Wireless Home/Away Smart Switch, with Netatmo, Light Almond | Wireless Home/Away Smart Switch, Light Almond |
| WNRL33NI | radiant® Wireless Home/Away Smart Switch, with Netatmo, Nickel | Wireless Home/Away Smart Switch, with, Nickel |
| WNRL33WH | radiant® Wireless Home/Away Smart Switch, with Netatmo, White | Wireless Home/Away Smart Switch, with, White |
| WNRH2LA | radiant® Smart Gateway Surface Mount with Netatmo, Light Almond | Smart Gateway Surface Mount with, Light Almond |
| WNRL33CKITBK | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Black | Smart Home/Away Switch with Netatmo, Black |
| WNRL33CKIT | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Brown | Smart Home/Away Switch with Netatmo, Brown |
| WNRL33CKITDB | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Dark Bronze | Smart Home/Away Switch with, Dark Bronze |
| WNRL33CKITG | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Graphite | Smart Home/Away Switch with Netatmo, Graphite |
| WNRL33CKITGRY | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Gray | Smart Home/Away Switch with Netatmo, Color, Gray |
| WNRL33CKITIV | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Ivory | Smart Home/Away Switch with Netatmo, Ivory |
| WNRL33CKITLA | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Light Almond | Smart Home/Away Switch with, Light Almond |
| WNRL33CKITNI | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, Nickel | Smart Home/Away Switch with Netatmo, Nickel |
| WNRL33CKITWH | radiant® Smart Home/Away Switch with Netatmo, Color Change Kit, White | Smart Home/Away Switch with Netatmo, White |
| WNRCB40CKITBK | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Black | Smart Scene Controller with Netatmo, Black |
| WNRCB40CKIT | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Brown | Smart Scene Controller with Netatmo, Brown |
| WNRCB40CKITDB | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Dark Bronze | Smart Scene Controller with, Dark Bronze |
| WNRCB40CKITG | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Graphite | Smart Scene Controller with Netatmo, Graphite |
| WNRCB40CKITGRY | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Gray | Smart Scene Controller with Netatmo, Color, Gray |
| WNRCB40CKITIV | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Ivory | Smart Scene Controller with Netatmo, Ivory |
| WNRCB40CKITLA | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Light Almond | Smart Scene Controller with, Light Almond |
| WNRCB40CKITNI | radiant® Smart Scene Controller with Netatmo, Color Change Kit, Nickel | Smart Scene Controller with Netatmo, Nickel |
| WNRCB40CKITWH | radiant® Smart Scene Controller with Netatmo, Color Change Kit, White | Smart Scene Controller with Netatmo, White |
| WNRL10CKITDB | radiant® Smart Switch with Netatmo, Color Change Kit, Dark Bronze | Smart Switch with Netatmo, Color, Dark Bronze |
| WNRL10CKITG | radiant® Smart Switch with Netatmo, Color Change Kit, Graphite | Smart Switch with Netatmo, Color, Graphite |
| WNRL10CKITLA | radiant® Smart Switch with Netatmo, Color Change Kit, Light Almond | Smart Switch with Netatmo, Color, Light Almond |
| WNRL10CKITNI | radiant® Smart Switch with Netatmo, Color Change Kit, Nickel | Smart Switch with Netatmo, Color Change, Nickel |
| WNRL50CKITDB | radiant® Smart Dimmer with Netatmo, Color Change Kit, Dark Bronze | Smart Dimmer with Netatmo, Color, Dark Bronze |
| WNRL50CKITG | radiant® Smart Dimmer with Netatmo, Color Change Kit, Graphite | Smart Dimmer with Netatmo, Color, Graphite |
| WNRL50CKITLA | radiant® Smart Dimmer with Netatmo, Color Change Kit, Light Almond | Smart Dimmer with Netatmo, Color, Light Almond |
| WNRL50CKITNI | radiant® Smart Dimmer with Netatmo, Color Change Kit, Nickel | Smart Dimmer with Netatmo, Color Change, Nickel |
| WNRL50LA | radiant® Smart Tru-Universal Dimmer with Netatmo, Light Almond | Smart Tru-Universal Dimmer with, Light Almond |
| WNRL43CKITBK | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Black | Smart Wake/Sleep Switch with Netatmo, Black |
| WNRL43CKIT | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Brown | Smart Wake/Sleep Switch with Netatmo, Brown |
| WNRL43CKITDB | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Dark Bronze | Smart Wake/Sleep Switch with, Dark Bronze |
| WNRL43CKITG | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Graphite | Smart Wake/Sleep Switch with Netatmo, Graphite |
| WNRL43CKITGRY | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Gray | Smart Wake/Sleep Switch with Netatmo, Gray |
| WNRL43CKITIV | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Ivory | Smart Wake/Sleep Switch with Netatmo, Ivory |
| WNRL43CKITNI | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Nickel | Smart Wake/Sleep Switch with Netatmo, Nickel |
| WNRL43CKITLA | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, Light Almond | Smart Wake/Sleep Switch with, Light Almond |
| WNRL43CKITWH | radiant® Smart Wake/Sleep Switch with Netatmo, Color Change Kit, White | Smart Wake/Sleep Switch with Netatmo, White |
| WNRL63CKITBK | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Black | Remote Smart Dimmer with Netatmo, Color, Black |
| WNRL63CKIT | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Brown | Remote Smart Dimmer with Netatmo, Color, Brown |
| WNRL63CKITDB | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Dark Bronze | Remote Smart Dimmer with Netatmo, Dark Bronze |
| WNRL63CKITG | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Graphite | Remote Smart Dimmer with Netatmo, Graphite |
| WNRL63CKITGRY | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Gray | Remote Smart Dimmer with Netatmo, Color, Gray |
| WNRL63CKITIV | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Ivory | Remote Smart Dimmer with Netatmo, Color, Ivory |
| WNRL63CKITLA | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Light Almond | Remote Smart Dimmer with Netatmo, Light Almond |
| WNRL63CKITNI | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, Nickel | Remote Smart Dimmer with Netatmo, Color, Nickel |
| WNRL63CKITWH | radiant® Remote Smart Dimmer with Netatmo, Color Change Kit, White | Remote Smart Dimmer with Netatmo, Color, White |
| WNRL23CKITBK | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Black | Remote Smart Switch with Netatmo, Color, Black |
| WNRL23CKIT | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Brown | Remote Smart Switch with Netatmo, Color, Brown |
| WNRL23CKITDB | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Dark Bronze | Remote Smart Switch with Netatmo, Dark Bronze |
| WNRL23CKITG | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Graphite | Remote Smart Switch with Netatmo, Graphite |
| WNRL23CKITGRY | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Gray | Remote Smart Switch with Netatmo, Color, Gray |
| WNRL23CKITIV | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Ivory | Remote Smart Switch with Netatmo, Color, Ivory |
| WNRL23CKITLA | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Light Almond | Remote Smart Switch with Netatmo, Light Almond |
| WNRL23CKITNI | radiant® Remote Smart Switch with Netatmo, Color Change Kit, Nickel | Remote Smart Switch with Netatmo, Color, Nickel |
| WNRL23CKITWH | radiant® Remote Smart Switch with Netatmo, Color Change Kit, White | Remote Smart Switch with Netatmo, Color, White |
| WNRL43LA | radiant® Wireless Wake/Sleep Smart Switch, with Netatmo, Light Almond | Wireless Wake/Sleep Smart Switch, Light Almond |
| WNRL43NI | radiant® Wireless Wake/Sleep Smart Switch, with Netatmo, Nickel | Wireless Wake/Sleep Smart Switch, with, Nickel |
| WNRL43WH | radiant® Wireless Wake/Sleep Smart Switch, with Netatmo, White | Wireless Wake/Sleep Smart Switch, with, White |
| WNRCB40LA | radiant® Wireless Smart Scene Controller with Netatmo, Light Almond | Wireless Smart Scene Controller, Light Almond |
| WNRCB40NI | radiant® Wireless Smart Scene Controller with Netatmo, Nickel | Wireless Smart Scene Controller with, Nickel |
| WNRCB40WH | radiant® Wireless Smart Scene Controller with Netatmo, White | Wireless Smart Scene Controller with, White |
| WNRL63LA | radiant® Wireless Remote Smart Dimmer, with Netatmo, Light Almond | Wireless Remote Smart Dimmer, with, Light Almond |
| WNRL23LA | radiant® Wireless Remote Smart Switch, with Netatmo, Light Almond | Wireless Remote Smart Switch, with, Light Almond |
| WNP20 | radiant® Plug-In Tru-Universal Smart Dimmer, with Netatmo, White | Plug-In Tru-Universal Smart Dimmer, with, White |
| NTL885TRBKCC6 | radiant® 15A Tamper-Resistant Outlet with Night Light, Black | 15A Tamper-Resistant Outlet with Night, Black |
| NTL885TRICC6 | radiant® 15A Tamper-Resistant Outlet with Night Light, Ivory | 15A Tamper-Resistant Outlet with Night, Ivory |
| NTL885TRLACC6 | radiant® 15A Tamper-Resistant Outlet with Night Light, Light Almond | 15A Tamper-Resistant Outlet with, Light Almond |
| NTL885TRNICC6 | radiant® 15A Tamper-Resistant Outlet with Night Light, Nickel | 15A Tamper-Resistant Outlet with Night, Nickel |
| NTL873LACC6 | radiant® Single Pole/3-Way Switch with Night Light, Light Almond | Single Pole/3-Way Switch with, Light Almond |
| TR26352RDBCC6 | radiant® Spec Grade 20A Tamper-Resistant Receptacle, Dark Bronze | Spec Grade 20A Tamper-Resistant, Dark Bronze |
| TR26352RGCC6 | radiant® Spec Grade 20A Tamper-Resistant Receptacle, Graphite | Spec Grade 20A Tamper-Resistant, Graphite |
| TR26352RLA | radiant® Spec Grade 20A Tamper-Resistant Receptacle, Light Almond | Spec Grade 20A Tamper-Resistant, Light Almond |
| R26USBPDBK | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Black | 15A Tamper Resistant Ultra Fast PLUS, Black |
| R26USBPD | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Brown | 15A Tamper Resistant Ultra Fast PLUS, Brown |
| R26USBPDCC6 | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Brown | 15A Tamper Resistant Ultra Fast PLUS, Brown |
| R26USBPDDBCC6 | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Dark Bronze | 15A Tamper Resistant Ultra Fast, Dark Bronze |
| R26USBPDGCC6 | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Graphite | 15A Tamper Resistant Ultra Fast PLUS, Graphite |
| R26USBPDGRY | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Gray | 15A Tamper Resistant Ultra Fast PLUS Power, Gray |
| R26USBPDI | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Ivory | 15A Tamper Resistant Ultra Fast PLUS, Ivory |
| R26USBPDLA | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Light Almond | 15A Tamper Resistant Ultra Fast, Light Almond |
| R26USBPDNICC6 | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Nickel | 15A Tamper Resistant Ultra Fast PLUS, Nickel |
| R26USBPDW | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, White | 15A Tamper Resistant Ultra Fast PLUS, White |
| R26USBPDWCC6 | radiant® 15A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, White | 15A Tamper Resistant Ultra Fast PLUS, White |
| TR20USBPDBK | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Black | 20A Tamper Resistant Ultra Fast PLUS, Black |
| TR20USBPD | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Brown | 20A Tamper Resistant Ultra Fast PLUS, Brown |
| TR20USBPDDB | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Dark Bronze | 20A Tamper Resistant Ultra Fast, Dark Bronze |
| TR20USBPDG | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Graphite | 20A Tamper Resistant Ultra Fast PLUS, Graphite |
| TR20USBPDGRY | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Gray | 20A Tamper Resistant Ultra Fast PLUS Power, Gray |
| TR20USBPDI | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Ivory | 20A Tamper Resistant Ultra Fast PLUS, Ivory |
| TR20USBPDLA | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Light Almond | 20A Tamper Resistant Ultra Fast, Light Almond |
| TR20USBPDNI | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Nickel | 20A Tamper Resistant Ultra Fast PLUS, Nickel |
| TR20USBPDRED | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, Red | 20A Tamper Resistant Ultra Fast PLUS Power, Red |
| TR20USBPDW | radiant® 20A Tamper Resistant Ultra Fast PLUS Power Delivery USB Type C/C Outlet, White | 20A Tamper Resistant Ultra Fast PLUS, White |
| R26USBPD65BK | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Black | 65W USB Outlet, Type C, 15A, Tamper-, Black |
| R26USBPD65 | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Brown | 65W USB Outlet, Type C, 15A, Tamper-, Brown |
| R26USBPD65W | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, White | 65W USB Outlet, Type C, 15A, Tamper-, White |
| R26USBPD65I | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Ivory | 65W USB Outlet, Type C, 15A, Tamper-, Ivory |
| R26USBPD65LA | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Light Almond | 65W USB Outlet, Type C, 15A, Tamper-, Light Almond |
| R26USBPD65GRY | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Gray | 65W USB Outlet, Type C, 15A, Tamper-, Gray |
| R26USBPD65NICC6 | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Nickel | 65W USB Outlet, Type C, 15A, Tamper-, Nickel |
| R26USBPD65GCC6 | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Graphite | 65W USB Outlet, Type C, 15A, Tamper-, Graphite |
| R26USBPD65DBCC6 | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, Dark Bronze | 65W USB Outlet, Type C, 15A, Tamper-, Dark Bronze |
| R26USBPD65WCC6 | radiant® 65W USB Outlet, Type C, 15A, Tamper-Resistant, White | 65W USB Outlet, Type C, 15A, Tamper-, White |
| TR20USBPD65I | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Ivory | 65W Commercial USB Outlet, Type C, 20A, Ivory |
| TR20USBPD65LA | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Light Almond | 65W Commercial USB Outlet, Type C, Light Almond |
| TR20USBPD65NI | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Nickel | 65W Commercial USB Outlet, Type C, 20A, Nickel |
| TR20USBPD65G | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Graphite | 65W Commercial USB Outlet, Type C, Graphite |
| TR20USBPD65DB | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Dark Bronze | 65W Commercial USB Outlet, Type C, Dark Bronze |
| TR20USBPD65RED | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Red | 65W Commercial USB Outlet, Type C, 20A, Red |
| TR20USBPD65BK | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Black | 65W Commercial USB Outlet, Type C, 20A, Black |
| TR20USBPD65 | radiant® 65W Commercial USB Outlet, Type C, 20A, Tamper-Resistant, Brown | 65W Commercial USB Outlet, Type C, 20A, Brown |
| TM870LASL | radiant® 15A Single-Pole Switch with Locator Light, Light Almond | 15A Single-Pole Switch with, Light Almond |
| R26USBAC6BK | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Black | 15A Tamper-Resistant Ultra-Fast USB Type, Black |
| R26USBAC6DBCCV4 | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Dark Bronze | 15A Tamper-Resistant Ultra-Fast USB, Dark Bronze |
| R26USBAC6G | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Graphite | 15A Tamper-Resistant Ultra-Fast USB, Graphite |
| R26USBAC6I | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Ivory | 15A Tamper-Resistant Ultra-Fast USB Type, Ivory |
| R26USBAC6LA | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Light Almond | 15A Tamper-Resistant Ultra-Fast, Light Almond |
| R26USBAC6NICCV4 | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, Nickel | 15A Tamper-Resistant Ultra-Fast USB Type, Nickel |
| R26USBAC6W | radiant® 15A Tamper-Resistant Ultra-Fast USB Type A/C Outlet, White | 15A Tamper-Resistant Ultra-Fast USB Type, White |
| R26USBCC6BK | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Black | 15A Tamper-Resistant Ultra-Fast USB Type, Black |
| R26USBCC6DBCCV4 | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Dark Bronze | 15A Tamper-Resistant Ultra-Fast USB, Dark Bronze |
| R26USBCC6G | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Graphite | 15A Tamper-Resistant Ultra-Fast USB, Graphite |
| R26USBCC6I | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Ivory | 15A Tamper-Resistant Ultra-Fast USB Type, Ivory |
| R26USBCC6LA | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Light Almond | 15A Tamper-Resistant Ultra-Fast, Light Almond |
| R26USBCC6NICCV4 | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, Nickel | 15A Tamper-Resistant Ultra-Fast USB Type, Nickel |
| R26USBCC6W | radiant® 15A Tamper-Resistant Ultra-Fast USB Type C/C Outlet, White | 15A Tamper-Resistant Ultra-Fast USB Type, White |
| R26USBACDBCCV4 | radiant® 15A Tamper-Resistant USB Type A/C Outlet, Dark Bronze | 15A Tamper-Resistant USB Type A/C, Dark Bronze |
| R26USBACLA | radiant® 15A Tamper-Resistant USB Type A/C Outlet, Light Almond | 15A Tamper-Resistant USB Type A/C, Light Almond |
| SS703 | Power Outlet Receptacle Openings, Two Gang, 302/304 Stainless Steel | Power Outlet Receptacle Openings, Two Gang |
| 3894WR | 50A Weather-Resistant Electrical Outlet for RVs / EV Chargers | 50A Weather-Resistant Electrical Outlet for RVs |

## Finish field / Product Name disagreements (56)

For these SKUs, the source `Finish` column's value does not appear anywhere in `Product Name` (checked case/hyphen-insensitive). Rather than guess which one is right, `LongDesc` keeps whatever color word (if any) is already in the Name text, unmodified. The `Finish` custom field (used for the multi-select finish filter) still uses the `Finish` column's value — so on these SKUs the filter facet and the display name may not visually agree. **Flag to Legrand's data team to confirm which column is correct.**

| BaseItemCode | Product Name | Finish field |
|---|---|---|
| AWP1G3PW4 | adorne® Matte White One-Gang-Plus Screwless Wall Plate with Microban® | Powder White |
| AWP1G2PW4 | adorne® Matte White One-Gang Screwless Wall Plate with Microban® | Powder White |
| AWP2GPW4 | adorne® Matte White Two-Gang Screwless Wall Plate with Microban® | Powder White |
| AWP3GPW4 | adorne® Matte White Three-Gang Screwless Wall Plate with Microban® | Powder White |
| AWP4GPW4 | adorne® Matte White Four-Gang Screwless Wall Plate with Microban® | Powder White |
| AWP5GPW1 | adorne® Matte White Five-Gang Screwless Wall Plate with Microban® | Powder White |
| AWP6GPW1 | adorne® Matte White Six-Gang Screwless Wall Plate with Microban® | Powder White |
| AFGF152TR | radiant® 15A TR AFCI/GFCI SELF-TEST RECEPT BN | Brown |
| AFGF152TRBK | radiant® 15A TR AFCI/GFCI SELF-TEST RECEPT BK | Black |
| AFGF152TRI | radiant® 15A TR AFCI/GFCI SELF-TEST RECEPT I | Ivory |
| AFGF152TRLA | radiant® 15A TR AFCI/GFCI SELF-TEST RECEPT LA | Light Almond |
| AFGF152TRW | radiant® 15A TR AFCI/GFCI SELF-TEST RECEPT W | White |
| AFGF202TR | radiant® 20A TR AFCI/GFCI SELF-TEST RECEPT BN | Brown |
| AFGF202TRBK | radiant® 20A TR AFCI/GFCI SELF TEST RECEPT BK | Black |
| AFGF202TRGRY | radiant® 20A TR AFCI/GFCI SELF TEST RECEPT GRY | Gray |
| AFGF202TRI | radiant® 20A TR AFCI/GFCI SELF-TEST RECEPT I | Ivory |
| AFGF202TRLA | radiant® 20A TR AFCI/GFCI SELF TEST RECEPT LA | Light Almond |
| RCD38TR | radiant® Single-Pole/3-Way Switch with 15A Tamper-Resistant Outlet | Brown |
| RCD11 | radiant® Two Single-Pole Switches | Brown |
| RCD113 | radiant® Two Single-Pole Switches & Single Pole/3-Way Switch | Brown |
| RCD33 | radiant® Two Single-Pole/3-Way Switches | Brown |
| 326RLA | radiant® BLANK INSERT LA | Light Almond |
| DIMBPASS | LED Dimmer Bypass Adapter | Black |
| RH1103PTC | radiant® INCAN SP/3W 1100W DIMMER, TC | Tri Color (WH, IV, LA) |
| RH4FBL3PTC | radiant® 0-10V LED/Fluorescent Dimmer | Tri Color (WH, IV, LA) |
| RHLV1103PTC | radiant® 120V, 1100VA Magnetic Low-Voltage Single Pole/3-Way Dimmer, Tri-Color | Tri Color (WH, IV, LA) |
| RHLV703PTC | radiant® 120V, 700VA, Magnetic Low-Voltage Single Pole/3-Way Dimmer, Tri-Color | Tri Color (WH, IV, LA) |
| RHFB83PTC | radiant® 2-Wire Fluorescent Dimmer, Tri-Color | Tri Color (WH, IV, LA) |
| RH703PTC | radiant® Incandescent 700W 3-Way Dimmer, Tri-Color | Tri Color (WH, IV, LA) |
| HMRTC | radiant® Multi-Location Remote Dimmer, Tri-Color | White |
| RHDH163PTC | radiant® Single-Pole/3-Way Fan Speed Control | Tri Color (WH, IV, LA) |
| RH703PTUTC | radiant® Tru-Universal Single Pole/3-Way Dimmer, Tri-Color | Tri Color (WH, IV, LA) |
| NTL885TRW | radiant® 15A Tamper-Resistant Outlet with Night Light | White |
| NTLHORZWCC6 | radiant® Horizontal Step Light | White |
| NTLFULLW | radiant® Night Light Full WH | White |
| RWP263BK | radiant® Three-Gang Screwless Wall Plate | Black |
| TM874GRY | radiant® 15A 4-Way Switch | Gray |
| RSWV153 | radiant® 15A Wave® Switch | Black |
| RSWV203 | radiant® 20A Wave® Switch | Black |
| TM870STMICC6 | radiant® Momentary Contact Switch | Ivory |
| TM870STMBKCC6 | radiant® Momentary Contact Switch | Black |
| TM870STMLACC6 | radiant® Momentary Contact Switch | Light Almond |
| TM870STMWCC6 | radiant® Momentary Contact Switch | White |
| R26USBCCDBCCV4 | radiant® 3.1 C-C USB+15A DUP REC DB VPK | Dark Bronze |
| RWP264WAMCC6 | radiant® Four-Gang Screwless Wall Plate with Microban® | White |
| RHCL453PWAMCC4 | radiant® LED/CFL Dimmer with Microban® | White |
| RWP26WAMCC6 | radiant® One-Gang Screwless Wall Plate with Microban® | White |
| RWP263WAMCC6 | radiant® Three-Gang Screwless Wall Plate with Microban® | White |
| RH703PTUWAMCC4 | radiant® Tru-Universal Dimmer with Microban® | White |
| RWP262WAMCC6 | radiant® Two-Gang Screwless Wall Plate with Microban® | White |
| 3894 | Straight Blade Receptacle 50A 125/250 3P 4W | Black |
| CP498TR15W | Single Kitchen Countertop Outlet TR 15A 125V W | White |
| CP498TR20W | Single Kitchen Countertop Outlet TR 20A 125V W | White |
| CP498TR15BK | Single Kitchen Countertop Outlet TR 15A 125V BK | Black |
| CP498TR20BK | Single Kitchen Countertop Outlet TR 20A 125V BK | Black |
| CP498LSS | Kitchen Countertop Outlet Lid Brushed Stainless SS | Stainless Steel |
