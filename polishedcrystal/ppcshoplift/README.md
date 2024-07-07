## ppcshoplift

Polished Crystal is open source.
Reading bits of the source sped up development to a sub-one-day project.

I've tested [`ppcshoplift.py`](ppcshoplift.py) on Mac and Windows.  You'll also need the `asm` directory (files I lifted from the Polished Crystal source). _NOTE: leave `asm` as a directory._

Directory structure should look like:

```
asm/attributes.asm
asm/item_constants.asm
asm/tmhm_constants.asm
ppcshoplift.py
savefile.sav
```

To run:

```bash
python3 ppcshoplist.py savefile.sav
```

Example session:

```
$ python3 ppcshoplift.py savefile.sav

Pokémon Polished Crystal 3.0.0-beta Offline Store v0.0.2
(Tested ROM (polishedcrystal-3.0.0-beta-22d6f8e1.gbc) md5sum 64276e3acc3fda02e0dcc235c9c2748a)

USE AT YOUR OWN PERIL!!!

Let's go shopping!


Main Menu

0.  Exit [and [over]write "newbag.sav"]
1.  Item
2.  Med
3.  Ball
4.  TH/HM
5.  Berry
6.  Key Item
7.  Apricorn
8.  Max Coins (current count: 30)
9.  [Over]write "newbag.sav" and continue shopping
10. Abort! (all changes since last write lost)

Selection: 2
```

`Item`, `Med`, `Ball`, `Berry`, `Apricorn` will increase any item selected to 99 whether you have any or not.  If zero it'll append to end of list if there is space.  If no space left, you'll be unable to add anymore items (only an issue with `Item`).  There is no option to set a quantity or delete/zero out.

E.g. increase both `RARE CANDY` and `REVIVAL HERB` to 99:

```
Med Menu (Select Med to increase to 99), 23 of 37 left

 0. Return             10. FRESH WATER:   5   20. MAX ETHER:     2   30. RAGECANDYBAR:  1
 1. ANTIDOTE:      3   11. FULL HEAL:    20   21. MAX POTION:   29   31. RARE CANDY:   79
 2. AWAKENING:     2   12. FULL RESTORE: 10   22. MAX REVIVE:    0   32. REVIVAL HERB:  0
 3. BURN HEAL:     2   13. HEAL POWDER:   0   23. MOOMOO MILK:   0   33. REVIVE:       19
 4. CALCIUM:       2   14. HP UP:         2   24. PARLYZ HEAL:   0   34. SACRED ASH:    0
 5. CARBOS:        2   15. HYPER POTION: 20   25. PEWTERCRUNCH:  0   35. SODA POP:      0
 6. ELIXIR:        3   16. ICE HEAL:      3   26. POTION:        9   36. SUPER POTION:  0
 7. ENERGY ROOT:   0   17. IRON:          1   27. PP MAX:        0   37. ZINC:          0
 8. ENERGYPOWDER:  0   18. LEMONADE:      0   28. PP UP:         2
 9. ETHER:         3   19. MAX ELIXIR:    1   29. PROTEIN:       2

Selection: 31

Med Menu (Select Med to increase to 99), 23 of 37 left

 0. Return             10. FRESH WATER:   5   20. MAX ETHER:     2   30. RAGECANDYBAR:  1
 1. ANTIDOTE:      3   11. FULL HEAL:    20   21. MAX POTION:   29   31. RARE CANDY:   99
 2. AWAKENING:     2   12. FULL RESTORE: 10   22. MAX REVIVE:    0   32. REVIVAL HERB:  0
 3. BURN HEAL:     2   13. HEAL POWDER:   0   23. MOOMOO MILK:   0   33. REVIVE:       19
 4. CALCIUM:       2   14. HP UP:         2   24. PARLYZ HEAL:   0   34. SACRED ASH:    0
 5. CARBOS:        2   15. HYPER POTION: 20   25. PEWTERCRUNCH:  0   35. SODA POP:      0
 6. ELIXIR:        3   16. ICE HEAL:      3   26. POTION:        9   36. SUPER POTION:  0
 7. ENERGY ROOT:   0   17. IRON:          1   27. PP MAX:        0   37. ZINC:          0
 8. ENERGYPOWDER:  0   18. LEMONADE:      0   28. PP UP:         2
 9. ETHER:         3   19. MAX ELIXIR:    1   29. PROTEIN:       2

Selection: 32

Med Menu (Select Med to increase to 99), 24 of 37 left

 0. Return             10. FRESH WATER:   5   20. MAX ETHER:     2   30. RAGECANDYBAR:  1
 1. ANTIDOTE:      3   11. FULL HEAL:    20   21. MAX POTION:   29   31. RARE CANDY:   99
 2. AWAKENING:     2   12. FULL RESTORE: 10   22. MAX REVIVE:    0   32. REVIVAL HERB: 99
 3. BURN HEAL:     2   13. HEAL POWDER:   0   23. MOOMOO MILK:   0   33. REVIVE:       19
 4. CALCIUM:       2   14. HP UP:         2   24. PARLYZ HEAL:   0   34. SACRED ASH:    0
 5. CARBOS:        2   15. HYPER POTION: 20   25. PEWTERCRUNCH:  0   35. SODA POP:      0
 6. ELIXIR:        3   16. ICE HEAL:      3   26. POTION:        9   36. SUPER POTION:  0
 7. ENERGY ROOT:   0   17. IRON:          1   27. PP MAX:        0   37. ZINC:          0
 8. ENERGYPOWDER:  0   18. LEMONADE:      0   28. PP UP:         2
 9. ETHER:         3   19. MAX ELIXIR:    1   29. PROTEIN:       2

Selection: 0
```

`TH/HM` and `Key Item` are bit fields that you simply toggle state.

E.g. add `SUPER_ROD` to Key Items:

```
Key Item Menu (Select Key Item to toggle bit)

 0. Return             8. SQUIRTBOTTLE: 1   16. LOST_ITEM:    0   24. OLD_SEA_MAP:  0
 1. BICYCLE:      1    9. SECRETPOTION: 0   17. RAINBOW_WING: 0   25. SHINY_CHARM:  0
 2. OLD_ROD:      1   10. RED_SCALE:    0   18. SILVER_WING:  0   26. OVAL_CHARM:   0
 3. GOOD_ROD:     1   11. CARD_KEY:     1   19. CLEAR_BELL:   1   27. CATCH_CHARM:  0
 4. SUPER_ROD:    0   12. BASEMENT_KEY: 1   20. GS_BALL:      0   28. SILPHSCOPE2:  0
 5. COIN_CASE:    1   13. S_S_TICKET:   1   21. BLUE_CARD:    1   29. APRICORN_BOX: 1
 6. ITEMFINDER:   1   14. PASS:         0   22. ORANGETICKET: 0   30. TYPE_CHART:   1
 7. MYSTERY_EGG:  0   15. MACHINE_PART: 0   23. MYSTICTICKET: 0

Selection: 4

Key Item Menu (Select Key Item to toggle bit)

 0. Return             8. SQUIRTBOTTLE: 1   16. LOST_ITEM:    0   24. OLD_SEA_MAP:  0
 1. BICYCLE:      1    9. SECRETPOTION: 0   17. RAINBOW_WING: 0   25. SHINY_CHARM:  0
 2. OLD_ROD:      1   10. RED_SCALE:    0   18. SILVER_WING:  0   26. OVAL_CHARM:   0
 3. GOOD_ROD:     1   11. CARD_KEY:     1   19. CLEAR_BELL:   1   27. CATCH_CHARM:  0
 4. SUPER_ROD:    1   12. BASEMENT_KEY: 1   20. GS_BALL:      0   28. SILPHSCOPE2:  0
 5. COIN_CASE:    1   13. S_S_TICKET:   1   21. BLUE_CARD:    1   29. APRICORN_BOX: 1
 6. ITEMFINDER:   1   14. PASS:         0   22. ORANGETICKET: 0   30. TYPE_CHART:   1
 7. MYSTERY_EGG:  0   15. MACHINE_PART: 0   23. MYSTICTICKET: 0

Selection: 0
```

Back to the main menu:

```
Main Menu

0.  Exit [and [over]write "newbag.sav"]
1.  Item
2.  Med
3.  Ball
4.  TH/HM
5.  Berry
6.  Key Item
7.  Apricorn
8.  Max Coins (current count: 30)
9.  [Over]write "newbag.sav" and continue shopping
10. Abort! (all changes since last write lost)

Selection:
```

Options `0`, `8`, `9`, and, `10` should be self-explanatory.

On exit (or write) `newbag.sav` will be created and your original input save file left unchanged.
