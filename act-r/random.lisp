(clear-all)

(load (translate-logical-pathname "ACT-R:model;util.lisp"))

(define-model random

(sgp :esc t)
(sgp :bll nil)
(sgp :ans 0.4)

(sgp :epl t)
;(sgp :pct t)
(sgp :ul t :egs 0.5)
(sgp :v nil)

(chunk-type stack-test-model main-state func-name func-state special-state start-no current-no next-no target-no search-dir)
(chunk-type maze-info from to f-west f-north f-east f-south b-west b-north b-east b-south)
(chunk-type search-dir-info dir-info)

(add-dm
  (stack-goal ISA stack-test-model main-state 0 special-state 0)
  (stack-goal-limit ISA stack-test-model special-state 1)
  (west ISA search-dir-info dir-info 0)
  (north ISA search-dir-info dir-info 1)
  (east ISA search-dir-info dir-info 2)
  (south ISA search-dir-info dir-info 3)
)

(P limit
  =goal>
    ISA					      stack-test-model
    special-state     1
  ==>
  =goal>
    ISA			          stack-test-model
    main-state        99
  !eval!            ("visit-points" (get-visited-points))
  !eval!            (clear-points)
  !output!          "limit!!"
)

(P stop
  =goal>
    ISA					  stack-test-model
    main-state	  0
    special-state 0
  ==>
  =goal>
    ISA			    stack-test-model
    main-state  99
    !eval!			("got-bored")
    !eval!      ("fired-judgement-rule")
)

(P continue
  =goal>
    ISA					  stack-test-model
    main-state	  0
    special-state 0
    !bind!        =current-start ("get-current-start")
    !bind!        =current-goal ("get-current-goal")
    !bind!        =reward ("get-reward-value")
  ==>
  =goal>
    ISA			      stack-test-model
    func-name		  "main"
    main-state	  1
    start-no		  =current-start
    target-no		  =current-goal
    !eval!			(visit-point =current-start)
    !eval!      (set-reward-value =reward)
    !eval!      ("fired-judgement-rule")
)

(P predict-terminate
  =goal>
    ISA				      stack-test-model
    main-state      99
  ==>
  =goal>
    ISA			        stack-test-model
    !eval!			    ("terminate")
)

(P predict1
  =goal>
    ISA					stack-test-model
    func-name		"main"
    main-state	1
    start-no		=start-no
  ?retrieval>
    state         free
  ==>
  =goal>
    ISA					stack-test-model
    main-state	2
    current-no	=start-no
)

(P predict2
  =goal>
    ISA						stack-test-model
    func-name			"main"
    main-state		2
    current-no	  =current-no
  ==>
  =goal>
    ISA					  stack-test-model
    main-state		3
  +retrieval>
    ISA           maze-info
    from			    =current-no
)

(P predict3-failure
  =goal>
    ISA				  stack-test-model
    func-name	  "main"
    main-state	3
    current-no	  =current-no
  ?retrieval>
    buffer      failure
  ==>
  =goal>
    ISA				  stack-test-model
    main-state	2
)

(P predict3
  =goal>
    ISA				        stack-test-model
    func-name		      "main"
    main-state	      3
  =retrieval>
    ISA				        maze-info
    to				        =to
  ==>
  =goal>
    ISA				        stack-test-model
    main-state	      4
    current-no        =to
  !safe-eval!     (visit-point =to)    
)

(P predict4
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state		4
    target-no		  =target-no
    current-no	  =current-no
    !safe-eval!	  (not (= =target-no =current-no))
  ==>
  =goal>
    ISA				    stack-test-model
    main-state		2
)

(P predict4-found
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state	  4
    target-no		  =target-no
    current-no	  =target-no
  ==>
  =goal>
    ISA				    stack-test-model
    main-state    10
  !output!		    "found!"
)

(P predict-clear
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state    10
  ==>
  =goal>
    ISA				    stack-test-model
    main-state    999
  !eval!			    ("clear")
)

(goal-focus stack-goal)

(spp continue :u 10.0)
(spp stop :u 5.0)
(spp predict-terminate :reward 0)
(spp predict2-west :u 10.0)
(spp predict2-north :u 10.0)
(spp predict2-east :u 10.0)
(spp predict2-south :u 10.0)
)