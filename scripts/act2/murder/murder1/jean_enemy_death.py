# Generated by BehavEd
# ( "PERSISTENCE--indicate jean_enemy has been defeated" )
waittimed ( 0.100 )
unlockCharacter("cyclops", "" )
waittimed ( 0.100 )
unlockCharacter("phoenix", "" )
setGameFlag("murder1", 3, 1 )
# ( "monster_undying--prevent deathscript from running more than once" )
check_jdeath = getZoneVar("jdeath" )
if check_jdeath == 0
     setZoneVar("jdeath", 1 )
     # ( "set up cut scene" )
     startCutScene("TRUE", "FALSE" )
     copyOriginAndAngles("jean_enemy", "wp_jean_go01" )
     moveHeroesToEnt("herospot02" )
     cameraFocusToEntity("cam_reveal", 384.000, 45.000, 300.000, 0.000 )
     waittimed ( 0.750 )
     cameraFocusToEntity("cam_reveal", 312.000, 45.000, 315.000, 2.000 )
     cameraFade(0.000, 1.000 )
     waittimed ( 0.750 )
     startConversation("act2/murder/murder1/2_murder1_020" )
endif

