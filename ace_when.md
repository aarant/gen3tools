goal: Call line 556 in p_anm_sys.c such that the index leads to OOB execution

this happens in function `ExecutePokeAnime(POKE_ANIME *pAnm)`:
```c
GF_ASSERT((u32)*(pAnm->SeqAdrs)<ANM_CMD_MAX&&"ERROR:AnimeCmdOver");`
func = PokeAnmCmdList[(u32)*(pAnm->SeqAdrs)];
func(pAnm);
```


pAnm->SeqAdrs is set in line 396 in function `void PokeAnm_SetPokeAnime(    POKE_ANM_SYS_PTR ptr, SOFT_SPRITE *ss, const P_ANM_SETTING_PARAM *inParam, const u8 inEntryIndex)`:
```c
    //Anime archive dataset
    ptr->PokeAnime[idx].ArcData =
        ArchiveDataLoadMallocLo(ARC_POKE_ANM, ptr->PokeAnime[idx].AnimeNo, ptr->HeapID );
    ptr->PokeAnime[idx].SeqAdrs = (u32*)ptr->PokeAnime[idx].ArcData;
```

I'm also interested in whether this check on line 376 exists in the release:
```c
    //Dealing with anime numbers outside the range
    if (anime_no >= POKE_ANIME_MAX){
        anime_no = 0;
        wait = 0;
    }
```

The animation number (animeNo) is set line 3921ish in poke_tool.c in function `void    PokePrgAnmDataSet(POKE_ANM_SYS_PTR pasp,SOFT_SPRITE *ss,u16 mons_no,int dir,int chr,int reverse,int index);`
```c
  ArchiveDataLoadOfs(&pat,ARC_POKE_ANM_TBL,0,mons_no*sizeof(POKE_ANM_TABLE),sizeof(POKE_ANM_TABLE));
  pas_p.AnimeNo=pat.poke_f.patno;
```
where it is set based on species number

This function, `PokePrgAnmDataSet`, and an apparent counterpart `PokeAnmDataSet`, that seems to copy data directly?, are called in a few places, but im mainly interested where they are called on the summary (in the leak, "status") screen

Here is the call chain for them:

- 288 in p_status.c  `PokeStatusProc_Init( PROC * proc, int * seq )` (apparently an initializer for the summary screen)
  - in pst_3d.c PokeStatus_SoftSpriteSet
    - PokeAnmDataSet

and

- 321 in p_status.c `PokeStatusProc_Main( PROC * proc, int * seq )` (i think this is a main loop for the summary screen)
   - 753 `PST_SeqIn( PST_WORK * wk )`
      - pst_3d.c PokeStatus_SoftSpriteAnmSet` (only called during "initial fade")
         - PokePrgAnmDataSet
