# Generated by BehavEd
# ( "comment" )
setGameFlag("doom4", 5, 1 )
spawnEffect("_ACTIVATOR_", "base/item/item_pickup", " 0.000 0.000 0.000 ", " 0.000 0.000 0.000 " )
sound (  "PLAY_SOUND", "common/game/pickup_item", "", "" )
remove ( "ultimate_nullifier", "ultimate_nullifier" )
objective ( "doom_obj60",  "EOBJCMD_COMPLETE" )
setEpilogue(11, 1 )
waittimed ( 0.100 )
sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
createPopupDialogXml("dialogs/special/nullifier_achievement" )

