# Generated by BehavEd
# ( "Heroes meet up with Dum Dum Dugan" )
act("dugan_spawn", "dugan_spawn" )
startCutScene("FALSE", "FALSE" )
cameraFocusToEntity("wp_wpdugan01", 600.000, 45.000, 0.000, 1.000 )
waittimed ( 0.750 )
setWaypointPath("dugan", "wpdugan", 1 )
waittimed ( 0.250 )
copyOriginAndAngles("_HERO1_", "h01" )
copyOriginAndAngles("_HERO2_", "h02" )
copyOriginAndAngles("_HERO3_", "h03" )
copyOriginAndAngles("_HERO4_", "h04" )
remove ( "h01", "h01" )
remove ( "h02", "h02" )
remove ( "h03", "h03" )
remove ( "h04", "h04" )
cameraFocusToEntity("wp_wpdugan01", 400.000, 45.000, 85.000, 3.000 )
controlPlayerHeroWithAI(-1.000 )
setWaypointPath("_HERO1_", "1hero", 1 )
setWaypointPath("_HERO2_", "2hero", 1 )
waittimed ( 0.125 )
setWaypointPath("_HERO3_", "3hero", 1 )
setWaypointPath("_HERO4_", "4hero", 1 )
waittimed ( 3.000 )
controlPlayerHeroWithAI(0.100 )
isWolvieHere = isActorOnTeam("wolverine" )
if isWolvieHere == 1
     setWaypointPath("_HERO1_", "", 1 )
     setWaypointPath("_HERO2_", "", 1 )
     setWaypointPath("_HERO3_", "", 1 )
     setWaypointPath("_HERO4_", "", 1 )
     waittimed ( 0.100 )
     sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
     createPopupDialogXml("dialogs/special/wolverinedugan_achievement" )
     waittimed ( 0.100 )
     startConversation("act1/omega/omega1/1_OMEGA1_022" )
else
     setWaypointPath("_HERO1_", "", 1 )
     setWaypointPath("_HERO2_", "", 1 )
     setWaypointPath("_HERO3_", "", 1 )
     setWaypointPath("_HERO4_", "", 1 )
     startConversation("act1/omega/omega1/1_OMEGA1_020" )
endif

