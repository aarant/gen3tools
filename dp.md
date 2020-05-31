## Addresses
| Symbol | Address |
| ------ | ------- |
| basePtr | 02106FAC |
| party  | +0xD2AC |

## Lua Info
- mode 1 = "Party"
- mode 2 = "Enemy"
- mode 3 = "Enemy 2"
- mode 4 = "Partner"
- mode 5 = "Wild"
- Each pokemon is 0xEC bytes

# Sprite ACE Kappa
- application/p_status.c
- 288 PokeStatusProc_Init( PROC * proc, int * seq )
  - PokeStatus_SoftSpriteSet
    - PokeAnmDataSet
- 321 PokeStatusProc_Main( PROC * proc, int * seq )
  - 753 PST_SeqIn( PST_WORK * wk )
    - calls during initial fade
    - PokeStatus_SoftSpriteAnmSet
      - PokePrgAnmDataSet
- application/pst_3d.c
- 722
- PokeStatus_SoftSpriteSet( PST_WORK * wk )
  - PokeAnmDataSet
- PokeStatus_SoftSpriteAnmSet( PST_WORK * wk )
  - PokePrgAnmDataSet
- poke_tool.c
- PokeAnmDataSet(SOFT_SPRITE_ANIME ssanm,u16 mons_no)
  - Seems to also load animation data?
- PokePrgAnmDataSet(POKE_ANM_SYS_PTR pasp,SOFT_SPRITE ss,u16 mons_no,int dir,int chr,int reverse,int index)
  - sets animation number, has check
- 3921
```c
//============================================================================================
/**
 *	Set Pokemon animation data (program animation)
 *
 * @param[in]	pasp	Animation system work pointer
 * @param[in]	ss		SoftSprite pointer to set animation data
 * @param[in]	monsno	Pokemon number to set
 * @param[in]	dir		Direction to set
 * @param[in]	chr		Pokemon personality (needed to determine back animation)
 * @param[in]	reverse	Whether to HFLIP? (PARA_HFLIP_OFF: without HFLIP PARA_HFLIP_ON: with HFLIP)
 * @param[in]	index	Index of system work to set
 */
//============================================================================================
void	PokePrgAnmDataSet(POKE_ANM_SYS_PTR pasp,SOFT_SPRITE *ss,u16 mons_no,int dir,int chr,int reverse,int index);  
```c
  ArchiveDataLoadOfs(&pat,ARC_POKE_ANM_TBL,0,mons_no*sizeof(POKE_ANM_TABLE),sizeof(POKE_ANM_TABLE));
  pas_p.AnimeNo=pat.poke_f.patno;
```
- pasp = ptr, pas_p=inParam, index=idx
- p_anm_sys.c
- SeqAdrs is Data sequence address
- POKE_ANIME_MAX = (50+84) = 134
- 376
```c
//Dealing with anime numbers outside the range
if (anime_no >= POKE_ANIME_MAX){
  anime_no = 0;
  wait = 0;
}
//Identify animation from monster number
ptr->PokeAnime[idx].AnimeNo = anime_no;
```
- 396
- ptr	= Pointer to Pokemon animation area
- idx = inEntryIndex	Registration index
```c
//Anime archive dataset
ptr->PokeAnime[idx].ArcData = ArchiveDataLoadMallocLo(ARC_POKE_ANM, ptr->PokeAnime[idx].AnimeNo, ptr->HeapID );
ptr->PokeAnime[idx].SeqAdrs = (u32*)ptr->PokeAnime[idx].ArcData;
```
- 556
```c
GF_ASSERT((u32)*(pAnm->SeqAdrs)<ANM_CMD_MAX&&"ERROR:AnimeCmdOver");
func = PokeAnmCmdList[(u32)*(pAnm->SeqAdrs)];
func(pAnm);
```
