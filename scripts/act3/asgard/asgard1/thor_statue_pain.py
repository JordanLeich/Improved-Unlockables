# Generated by BehavEd
# ( "Only Thor can use his statue" )
name = getName("_ACTIVATOR_" )
if name == "thor"
     waittimed ( 0.100 )
     sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
     createPopupDialogXml("dialogs/special/thorhammer_achievement" )
     waittimed ( 0.100 )
     remove ( "brick_relay_tom", "brick_relay_tom" )
     act("brick_relay03", "brick_relay03" )
endif
