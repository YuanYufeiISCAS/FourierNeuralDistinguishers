# The code for paper "Fourier Analysis of Neural Distinguishers"

Update time: 

- 2025-09-02: first commit
- 2025-10-11: upload the main code
- 2026-03-30: update  README



At present, it only includes the experimental code used in the paper.  I plan to clean it up and package it as a tool when time permits. And if you have any problem about our code (or paper), please feel free to contact me (yufei2021@iscas.ac.cn). 



## Table of Content

```
anonymous_submission
  │  README.md
  │
  ├─main (Main codes in our work.)
  │   ├─README.md (The descriptions.)
  │   │
  │   ├─core (The main code to reproduce our results.)
  │   │  
  │   └─example (The example in CNF)
  │         
  └─QuickVerify (The code for verifying DL-relevant results.)
      ├─DLvariant
      │
      └─NeuralD/speck (The Speck32/64 distinguishers we use to analyze.)
```



## BibTeX

```
@article{Yuan_Wu_Zhang_Wu_2026, 
	title={Fourier Analysis of Neural Distinguishers}, 
	volume={2026}, 
	url={https://tosc.iacr.org/index.php/ToSC/article/view/12792}, 
	DOI={10.46586/tosc.v2026.i1.441-467}, 
	number={1}, 
	journal={IACR Transactions on Symmetric Cryptology}, 
	author={Yuan, Yufei and Wu, Wenling and Zhang, Lei and Wu, Ruichen}, 		year={2026}, 
	month={Mar.}, 
	pages={441–467} }
```



## Notice

The codes including ResNet design and Speck encryption are cited from [33].

The weights of 7-, 8-round Speck32/64 ND and 10-round Simon ND are cited from [26].

The repository also contains 8-round, 9-round Speck32/64 ND parameter, if you use the relevant distinguishers or results, please cite our paper "Rethinking Learning-based Symmetric Cryptanalysis: a Theoretical Perspective" (https://eprint.iacr.org/2025/1306) with:

```
@misc{cryptoeprint:2025/1306,
      author = {Yufei Yuan and Haiyi Xu and Jiaye Teng and Lei Zhang and Wenling Wu},
      title = {Rethinking Learning-based Symmetric Cryptanalysis: a Theoretical Perspective},
      howpublished = {Cryptology {ePrint} Archive, Paper 2025/1306},
      year = {2025},
      url = {https://eprint.iacr.org/2025/1306}
}
```

