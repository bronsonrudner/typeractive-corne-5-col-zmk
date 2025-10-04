#pragma once

#define __ &trans

#define _a &kp A
#define _b &kp B
#define _c &kp C
#define _d &kp D
#define _e &kp E
#define _f &kp F
#define _g &kp G
#define _h &kp H
#define _i &kp I
#define _j &kp J
#define _k &kp K
#define _l &kp L
#define _m &kp M
#define _n &kp N
#define _o &kp O
#define _p &kp P
#define _q &kp Q
#define _r &kp R
#define _s &kp S
#define _t &kp T
#define _u &kp U
#define _v &kp V
#define _w &kp W
#define _x &kp X
#define _y &kp Y
#define _z &kp Z

#define _A &kp LS(A)
#define _B &kp LS(B)
#define _C &kp LS(C)
#define _D &kp LS(D)
#define _E &kp LS(E)
#define _F &kp LS(F)
#define _G &kp LS(G)
#define _H &kp LS(H)
#define _I &kp LS(I)
#define _J &kp LS(J)
#define _K &kp LS(K)
#define _L &kp LS(L)
#define _M &kp LS(M)
#define _N &kp LS(N)
#define _O &kp LS(O)
#define _P &kp LS(P)
#define _Q &kp LS(Q)
#define _R &kp LS(R)
#define _S &kp LS(S)
#define _T &kp LS(T)
#define _U &kp LS(U)
#define _V &kp LS(V)
#define _W &kp LS(W)
#define _X &kp LS(X)
#define _Y &kp LS(Y)
#define _Z &kp LS(Z)

#define _0 &kp N0
#define _1 &kp N1
#define _2 &kp N2
#define _3 &kp N3
#define _4 &kp N4
#define _5 &kp N5
#define _6 &kp N6
#define _7 &kp N7
#define _8 &kp N8
#define _9 &kp N9

#define _f1 &kp F1
#define _f2 &kp F2
#define _f3 &kp F3
#define _f4 &kp F4
#define _f5 &kp F5
#define _f6 &kp F6
#define _f7 &kp F7
#define _f8 &kp F8
#define _f9 &kp F9
#define _f10 &kp F10
#define _f11 &kp F11
#define _f12 &kp F12

#define _min &kp MINUS
#define _und &kp UNDERSCORE
#define _sqt &kp SQT
#define _dqt &kp GB_DQT
#define _dot &kp DOT
#define _com &kp COMMA
#define _fsl &kp FSLH
#define _bsl &kp GB_BSLH
#define _at &kp GB_AT
#define _qu &kp QUESTION
#define _til &kp GB_TILDE
#define _grv &kp GRAVE
#define _hash &kp GB_HASH
#define _dlr &kp DLLR

#define _esc &kp ESC
#define _tab &kp TAB
#define _ent &kp ENTER

// nav keys
#define _hm &kp HOME
#define _pgup &kp PG_UP
#define _pgdn &kp PG_DN
#define _end &kp END
#define _ins &kp INSERT
#define _left &kp LEFT
#define _up &kp UP
#define _down &kp DOWN
#define _rght &kp RIGHT
#define _vdn &kp C_VOL_DN
#define _vup &kp C_VOL_UP

// home row mods
// default layer
#define __c &hlm LALT C
#define __i &hlm LWIN I
#define __e &hls LCTRL E
#define __a &hls LSHFT A
#define __h &hls RSHFT H
#define __t &hls RCTRL T
#define __n &hlm RWIN N
#define __s &hlm LALT S
// CAP layer
#define __E &hls LCTRL LS(E)
// NAV layer
#define __0 &hlm LALT N0
#define __4 &hlm LWIN N4
#define __5 &hls LCTRL N5
#define __6 &hls LSHFT N6
// NUM layer
#define __f5 &hlm LALT F5
#define __f6 &hlm LWIN F6
#define __f7 &hls LCTRL F7
#define __f8 &hls LSHFT F8

// thumb keys
#define __ent &lt LCAP ENTER
#define __spc &lt LFUN SPACE
#define __r &lt LNAV R
#define __R &lt LNAV LS(R)
#define _tap &sl LTAP
