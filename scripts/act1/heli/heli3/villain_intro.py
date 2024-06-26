# Generated by BehavEd
startCutScene("FALSE", "FALSE" )
faceEntity("ff_striker01", "console01" )
faceEntity("ff_striker02", "console02" )
cameraMove(" -846.830 -196.050 224.250 ", 2.000 )
cameraPan(" 0.000 46.500 73.200 ", 2.000, "FALSE" )
waittimed ( 1.000 )
faceEntity("ws01", "console01" )
faceEntity("rm01", "console02" )
waittimed ( 1.000 )
moveHeroesToEnt("hero_spot01" )
waittimed ( 0.500 )
sound (  "PLAY_SOUND", "Zone_shared/heli/console", "", "" )
playanim (  "EA_USE_BUTTON", "ff_striker01", "NONE", "" )
playanim (  "EA_USE_BUTTON", "ff_striker02", "NONE", "animsig01" )
waitsignal ( "animsig01" )
remove ( "ff_button01", "ff_button01" )
remove ( "ff_button02", "ff_button02" )
cameraMove(" -272.390 -533.370 226.800 ", 1.000 )
cameraPan(" 0.000 45.000 0.000 ", 1.000, "FALSE" )
waittimed ( 1.000 )
spawnEffect("ff_spot02", "map/heli/forcefield_20ft_expire", " 0.000 0.000 0.000 ", " 0.000 0.000 0.000 " )
waittimed ( 0.250 )
copyOriginAndAngles("force_field02", "ff_spot02" )
waittimed ( 1.000 )
faceEntity("ws01", "hero_spot01" )
faceEntity("rm01", "hero_spot01" )
cameraMove(" -434.890 -589.730 181.340 ", 1.000 )
cameraPan(" 0.000 33.100 157.900 ", 1.000, "FALSE" )
waittimed ( 1.000 )
remove ( "ff_striker01", "ff_striker01" )
remove ( "ff_striker02", "ff_striker02" )
isHere = isActorOnTeam("captainamerica" )
DoomisHere = isActorOnTeam("doomdlc")
if DoomisHere == 1
	# ( "Play this conversation if doom is on the team" )
    sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
    createPopupDialogXml("dialogs/special/doomwinter_achievement" )
    waittimed ( 0.100 )
	startConversation("act1/heli/heli3/1_heli3_030_DLC" )
else
	if isHere == 1
	     # ( "Play this conversation if CAP is on the team" )
	     startConversation("act1/heli/heli3/1_heli3_040" )
	else
	     isHere = isActorOnTeam("thor" )
	     if isHere == 1
		  # ( "Play this conversation if CAP not on the team, But Thor IS" )
		  startConversation("act1/heli/heli3/1_heli3_050" )
	     else
		  # ( "Play this conversation if both thor and Cap are not here" )
		  startConversation("act1/heli/heli3/1_heli3_030" )
	     endif
	endif
endif

