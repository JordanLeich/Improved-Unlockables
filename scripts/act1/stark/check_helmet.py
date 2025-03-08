got_helmet = getGameFlag("conv_vars", 14 )
run_once = getObjective("Stark_Obj20", "COMPLETE" )
if run_once == 0
     if got_helmet == 1
          objective ( "Stark_Obj20",  "EOBJCMD_COMPLETE" )
          allowConversation("TRUE" )
          unlockCharacter("gman", "" )
          waittimed ( 0.500 )
          unlockCharacter("hulk", "" )
     else
          allowConversation("FALSE" )
     endif
else
     allowConversation("FALSE" )
endif