# Generated by BehavEd
# ( "comment" )
sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
createPopupDialogXml("dialogs/special/fingfangfoom_achievement" )
waittimed ( 0.100 )
awardAchievement("", "defeated_fingfangfoom" )
waittimed ( 0.100 )

nickfury = isActorOnTeam("Nickfury" )
if nickfury == 0
    awardAchievement("", "unlocked_nickfury" )
    waittimed ( 0.100 )
    unlockCharacter("nickfury", "" )
    waittimed ( 0.100 )
    sound (  "PLAY_SOUND", "common/game/achievement", "", "" )
    createPopupDialogXml("dialogs/special/nickfury_achievement" )
    waittimed ( 0.100 )
endif

unlockCharacter("Taskmaster", "" )
waittimed ( 0.100 )
unlockCharacter("storm", "" )
waittimed ( 0.100 )
unlockCharacter("Warmachine", "" )
waittimed ( 0.100 )
unlockCharacter("sable", "" )
waittimed ( 0.100 )
unlockCharacter("ted", "" )
waittimed ( 0.100 )
unlockCharacter("devilhulk", "" )
waittimed ( 0.100 )
unlockCharacter("greenscar", "" )
waittimed ( 0.100 )
unlockCharacter("banner", "" )
waittimed ( 0.100 )
unlockCharacter("ferhul", "" )
waittimed ( 0.100 )
unlockCharacter("mergedhulk", "" )
waittimed ( 0.100 )
unlockCharacter("ted", "" )
waittimed ( 0.100 )
unlockCharacter("hellion", "" )
waittimed ( 0.100 )
unlockCharacter("visiondlc", "" )
waittimed ( 0.100 )
unlockCharacter("ironman", "" )
waittimed ( 0.100 )
unlockCharacter("ironheart", "" )
waittimed ( 0.100 )
unlockCharacter("yelena", "" )
waittimed ( 0.100 )
unlockCharacter("blackwidowv", "" )
waittimed ( 0.100 )
unlockCharacter("Kate", "" )
waittimed ( 0.100 )
unlockCharacter("HumanTorch", "" )
waittimed ( 0.100 )
unlockCharacter("MrFantastic", "" )
waittimed ( 0.100 )
unlockCharacter("Hawkeye", "" )
objective ( "heli_obj40",  "EOBJCMD_COMPLETE" )

