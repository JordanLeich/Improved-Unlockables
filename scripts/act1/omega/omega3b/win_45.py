# Generated by BehavEd
# ( "comment" )
objective ( "omega_obj45",  "EOBJCMD_COMPLETE" )
waittimed ( 0.100 )
sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
createPopupDialogXml("dialogs/special/protectcomputer_achievement" )
waittimed ( 0.100 )
setEpilogue(1, 1 )
setHintType("protect_me", "none" )
showHealthBar("protect_me", "FALSE" )

