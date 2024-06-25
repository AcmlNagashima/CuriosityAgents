(clear-all)

(load (translate-logical-pathname "ACT-R:model;util.lisp"))

(define-model instance-base

(sgp :esc t)
(sgp :bll nil)
(sgp :ans 0.4)

(sgp :epl t)
;(sgp :pct t)
(sgp :ul t :egs 0.5)
(sgp :v nil)
(sgp :cia t)
(sgp :rir nil)

(chunk-type remembered-road road-no road-foward-no)
(chunk-type stack-element data pre)
(chunk-type path-element path-data path-next)
(chunk-type stack-data stack-data-from stack-data-to stack-data-west stack-data-north stack-data-east stack-data-south)
(chunk-type stack-test-model main-state func-name func-state special-state checked-west checked-north checked-east checked-south in-data tail result result-data start-no current-no target-no)
(chunk-type maze-info from to f-west f-north f-east f-south b-west b-north b-east b-south)

(add-dm
  (stack-goal ISA stack-test-model main-state 0 special-state 0)
  (stack-goal-limit ISA stack-test-model special-state 1)
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
  ==>
  =goal>
    ISA           stack-test-model
    main-state    40
    current-no    =start-no
    checked-west  -1
    checked-north -1
    checked-east  -1
    checked-south -1
    tail          nil
)

(P select-tactics
  =goal>
    ISA					stack-test-model
    func-name		"main"
    main-state	40
    current-no  =current-no
  ?retrieval>
    state         free
  ==>
  =goal>
    ISA					stack-test-model
    main-state	41
  +retrieval>
    ISA         remembered-road
    road-no			=current-no
)

(P selected-random
  =goal>
    ISA					stack-test-model
    func-name		"main"
    main-state	41
  ?retrieval>
    buffer        failure
  ==>
  =goal>
    ISA					stack-test-model
    main-state	2
)

(P selected-cased-base
  =goal>
    ISA					    stack-test-model
    func-name		    "main"
    main-state	    41
  ?retrieval>
    buffer full  
  ==>
  =goal>
    ISA             stack-test-model
    main-state	    42
)

(P move-cased-base
  =goal>
    ISA					    stack-test-model
    func-name		    "main"
    main-state	    42
    current-no      =current-no
  =retrieval>
    ISA             remembered-road
    road-foward-no  =road-foward-no
  ==>
  =goal>
    ISA             stack-test-model
    current-no      =road-foward-no
    main-state	    43
    !safe-eval!     (visit-point =road-foward-no)
)

(P end-cased-base
  =goal>
    ISA					    stack-test-model
    func-name		    "main"
    main-state	    42
    current-no      =current-no
  ?retrieval>
    buffer          failure
  ==>
  =goal>
    ISA           stack-test-model
    start-no      =current-no
    main-state    1
)

(P move-cased-base-found
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state	  43
    current-no    =current-no
    target-no     =current-no
  ==>
  =goal>
    ISA				    stack-test-model
    func-name		  "create-goal-path"
    main-state    10
    func-state    1
  !output!		    "cased-base-found!"
)

(P move-cased-base-not-found
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state	  43
    target-no		  =target-no
    current-no	  =current-no
    !safe-eval!	  (not (= =target-no =current-no))
  ==>
  =goal>
    ISA				    stack-test-model
    main-state    42
  +retrieval>
    ISA           remembered-road
    road-no			  =current-no
)

(P backtrack-start
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state		30
  ==>
  =goal>
    ISA				    stack-test-model
    main-state		31
    func-name		  "pop"
    func-state		1
)

(P backtrack1
  =goal>
    ISA				  stack-test-model
    func-name		"main"
    main-state	31
    result			=result
  ==>
  =goal>
    ISA				  stack-test-model
    main-state	32
    +retrieval>	=result
)

(P backtrack1-nil
  =goal>
    ISA				  stack-test-model
    func-name		"main"
    main-state	31
    result			nil
  ==>
  =goal>
    ISA				  stack-test-model
    checked-west  -1
    checked-north -1
    checked-east  -1
    checked-south -1
    tail				  nil
    main-state	  2
)

(P backtrack2-failure
  =goal>
    ISA			      stack-test-model
    func-name		  "main"
    main-state	  32
  ?retrieval>
    buffer        failure
  ==>
  =goal>
    ISA				    stack-test-model
    main-state		31
)

(P backtrack2
  =goal>
    ISA			      stack-test-model
    func-name		  "main"
    main-state	  32
  =retrieval>
    ISA				    stack-element
    data			    =data
  ==>
  =goal>
    ISA				    stack-test-model
    main-state		33
    result-data		=data
  +retrieval>			=data
)

(P backtrack-end-failure
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state	  33
    result-data   =result-data
  ?retrieval>
    buffer   		  failure
  ==>
  =goal>
    ISA				    stack-test-model
  +retrieval>			=result-data
)

(P backtrack-end
  =goal>
    ISA				                stack-test-model
    func-name		              "main"
    main-state		            33
  =retrieval>
    ISA				                stack-data
    stack-data-from	          =stack-data-from
    stack-data-to	            =stack-data-to
    stack-data-west           =stack-data-west
    stack-data-north          =stack-data-north
    stack-data-east           =stack-data-east
    stack-data-south          =stack-data-south
  ==>
  =goal>
    ISA				      stack-test-model
    main-state		  2
    current-no      =stack-data-from
    checked-west    =stack-data-west
    checked-north   =stack-data-north
    checked-east    =stack-data-east
    checked-south   =stack-data-south
    !safe-eval!     (visit-point =stack-data-from)
  -retrieval>
)

(P predict2
  =goal>
    ISA						stack-test-model
    func-name			"main"
    main-state		2
    current-no	  =current-no
    checked-west  =checked-west
    checked-north =checked-north
    checked-east  =checked-east
    checked-south =checked-south
  ==>
  =goal>
    ISA					  stack-test-model
    main-state		3
  +retrieval>
    ISA           maze-info
    from			    =current-no
    - f-west      =checked-west
    - f-north     =checked-north
    - f-east      =checked-east
    - f-south     =checked-south
)

(P predict3-west
  =goal>
    ISA				        stack-test-model
    func-name		      "main"
    main-state	      3
  =retrieval>
    ISA				        maze-info
    f-west            1
  ==>
  =retrieval>
  =goal>
    ISA				        stack-test-model
    main-state	      5
    checked-west      1
)

(P predict3-north
  =goal>
    ISA				        stack-test-model
    func-name		      "main"
    main-state	      3
  =retrieval>
    ISA				        maze-info
    f-north           1
  ==>
  =retrieval>
  =goal>
    ISA				        stack-test-model
    main-state	      5
    checked-north     1
)

(P predict3-east
  =goal>
    ISA				        stack-test-model
    func-name		      "main"
    main-state	      3
  =retrieval>
    ISA				        maze-info
    f-east            1
  ==>
  =retrieval>
  =goal>
    ISA				        stack-test-model
    main-state	      5
    checked-east      1
)

(P predict3-south
  =goal>
    ISA				        stack-test-model
    func-name		      "main"
    main-state	      3
  =retrieval>
    ISA				        maze-info
    f-south           1
  ==>
  =retrieval>
  =goal>
    ISA				        stack-test-model
    main-state	      5
    checked-south     1
)

;; go to backtrack
(P predict3-failure
  =goal>
    ISA				  stack-test-model
    func-name	  "main"
    main-state	3
  ?retrieval>
    buffer      failure
  ==>
  =goal>
    ISA				  stack-test-model
    main-state	30
)

(P predict5
  =goal>
    ISA					      stack-test-model
    func-name		      "main"
    main-state	      5
    current-no	      =current-no
    checked-west      =checked-west
    checked-north     =checked-north
    checked-east      =checked-east
    checked-south     =checked-south
  =retrieval>
    ISA               maze-info
    to                =to
  ?imaginal>
    state		          free    
  ==>
  =retrieval>
  =goal>
    ISA					      stack-test-model
    main-state	      6
  +imaginal>
    ISA               stack-data
    stack-data-from   =current-no
    stack-data-to     =to
    stack-data-west   =checked-west
    stack-data-north  =checked-north
    stack-data-east   =checked-east
    stack-data-south  =checked-south
)

(P predict6
  =goal>
    ISA				  stack-test-model
    func-name		"main"
    main-state	6
  =retrieval>
    ISA         maze-info
    to          =to
    b-west      =b-west
    b-north     =b-north
    b-east      =b-east
    b-south     =b-south
  =imaginal>
  ==>
  =goal>
    ISA             stack-test-model
    main-state      9
    current-no      =to
    checked-west    =b-west
    checked-north   =b-north
    checked-east    =b-east
    checked-south   =b-south
    in-data         =imaginal
    func-name       "push"
    func-state      1
 !safe-eval!        (visit-point =to) 
)

(P predict9
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state		9
    target-no		  =target-no
    current-no	  =current-no
    !safe-eval!	  (not (= =target-no =current-no))
  ==>
  =goal>
    ISA				    stack-test-model
    main-state		40
)

(P predict9-found
  =goal>
    ISA				    stack-test-model
    func-name		  "main"
    main-state	  9
    target-no		  =target-no
    current-no	  =target-no
  ==>
  =goal>
    ISA				    stack-test-model
    main-state    10
    func-name		  "create-goal-path"
    func-state    1
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

;;プッシュ機能
(P push-stack-failure
  =goal>
    ISA			    stack-test-model
    func-name	  "push"
  ?retrieval>
    buffer      failure
  ==>
  =goal>
    ISA			    stack-test-model
    func-state	1		
)

(P push-stack-busy
  =goal>
    ISA			    stack-test-model
    func-name	  "push"
  ?imaginal>
    state		    busy
  ==>
)

(P push-stack1-first
  =goal>
    ISA			    stack-test-model
    func-name	  "push"
    func-state	1
    in-data	    =in-data
    tail		    nil
  ?imaginal>
    state		    free
  ==>
  =goal>
    ISA			    stack-test-model
    func-name	  "push"
    func-state	2
  +imaginal>
    ISA         stack-element
    data		    =in-data
    pre			    nil
)

(P push-stack1
  =goal>
    ISA					stack-test-model
    func-name		"push"
    func-state	1
    in-data		  =in-data
    tail				=tail
  ?imaginal>
    state		    free
  ==>
  =goal>
    ISA					stack-test-model
    func-name		"push"
    func-state	2
  +imaginal>
    ISA         stack-element
    data			  =in-data
    pre				  =tail
)

(P push-stack2
  =goal>
    ISA					stack-test-model
    func-name		"push"
    func-state	2
  ?imaginal>
    state				free
  =imaginal>
  ==>
  =goal>
    ISA					stack-test-model
    tail				=imaginal
    func-state	99
  -imaginal>
)

;;ポップ機能
(P pop-stack-failure
  =goal>
    ISA			    stack-test-model
    func-name	  "pop"
  ?retrieval>
    buffer      failure
  ==>
    =goal>
    ISA			    stack-test-model
    func-state	1
)

(P pop-stack-nil
  =goal>
    ISA						stack-test-model
    func-name			"pop"
    func-state		1
    tail					nil
  ==>
  =goal>
    ISA						stack-test-model
    result				nil
    func-state		99
)

(P pop-stack1
  =goal>
    ISA			      stack-test-model
    func-name	    "pop"
    func-state	  1
    tail		      =tail
  ==>
  =goal>
    ISA			      stack-test-model
    func-state	  2
    +retrieval>	  =tail
)

(P pop-stack2-nil
  =goal>
    ISA					stack-test-model
    func-name		"pop"
    func-state	2
    tail				=tail
  =retrieval>
    ISA         stack-element
    pre					nil
  ==>
  =goal>
    ISA					stack-test-model
    result			=tail
    tail				nil
    func-state	99
)

(P pop-stack2
  =goal>
    ISA			    stack-test-model
    func-name	  "pop"
    func-state	2
    tail		    =tail
  =retrieval>
    ISA         stack-element
    pre				  =pre
  ==>
  =goal>
    ISA			    stack-test-model
    result		  =tail
    tail			   =pre
    func-state	  99
)

(P func-end
  =goal>
    ISA					stack-test-model
    func-state	99
  ==>
  =goal>
    ISA					stack-test-model
    func-name		"main"
    func-state	0
)

;;ゴールまでのパス作成
(P create-goal-path-failure
  =goal>
    ISA				  stack-test-model
    func-name		"create-goal-path"
  ?retrieval>
    buffer 			failure
  ==>
  =goal>
    ISA				  stack-test-model
    func-state	1
)

(P create-goal-path1-nil
  =goal>
    ISA				  stack-test-model
    func-name		"create-goal-path"
    func-state	1
    tail			  nil
  ==>
  =goal>
    ISA				    stack-test-model
    func-name		  "create-goal-path"
    func-state		99
)

(P create-goal-path1
  =goal>
    ISA				    stack-test-model
    func-name		  "create-goal-path"
    func-state	  1
    tail			    =tail
  ==>
  =goal>
    ISA				    stack-test-model
    func-state	  2
    +retrieval>	  =tail
)

(P create-goal-path2
  =goal>
    ISA				    stack-test-model
    func-name		  "create-goal-path"
    func-state	  2
  =retrieval>
    ISA           stack-element
    data			    =data
    pre				    =pre
  ==>
  =goal>
    ISA				    stack-test-model
    func-state	  3
    tail          =pre
  +retrieval>			=data
)

(P create-goal-path2-nil
  =goal>
    ISA				    stack-test-model
    func-name		  "create-goal-path"
    func-state	  2
  =retrieval>
    ISA           stack-element
    data			    =data
    pre				    nil
  ==>
  =goal>
    ISA				    stack-test-model
    func-state	  3
    tail          nil
  +retrieval>			=data
)

(P create-goal-path3
  =goal>
    ISA				        stack-test-model
    func-name		      "create-goal-path"
    func-state	      3
  =retrieval>
    ISA               stack-data
    stack-data-from	  =from-no
    stack-data-to			=to-no
  ?imaginal>
    state			        free
  ==>
  =goal>
    ISA				      stack-test-model
    func-state	    1
  +imaginal>
    ISA				      remembered-road
    road-no			    =from-no
    road-foward-no	=to-no
)
)