# Generated by BehavEd
# ( "comment" )
waittimed ( 0.100 )
sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
createPopupDialogXml("dialogs/special/kelp_achievement" )
waittimed ( 0.100 )
unlockCharacter("submariner", "" )
waittimed ( 0.100 )
unlockCharacter("namorita2", "" )
startCutScene("FALSE", "FALSE" )
cameraFade(1.000, 1.000 )
waittimed ( 1.000 )
objective ( "atlantis_obj40",  "EOBJCMD_COMPLETE" )
setEpilogue(2, 1 )
setGameFlag("atlantis1", 4, 1 )
remove ( "namorita", "namorita" )
remove ( "namorbubble", "namorbubble" )
cameraFade(0.000, 1.000 )
waittimed ( 1.000 )
endCutScene("FALSE", "TRUE" )

