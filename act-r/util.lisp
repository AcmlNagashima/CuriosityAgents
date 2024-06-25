;We modify the function in ACT-R 7.21 to not inherit those triggers after the compilation and assign the reward trigger at any time point after the production compilation occurred.
;http://act-r.psy.cmu.edu/actr7.21/actr7.x.zip
(defun initialize-utility-for-compiled-production (new-p p1 p2)
  (trigger-reward *reward-value*)
  (let* ((at1 (production-at p1))
         (at2 (production-at p2))
         (at (max at1 at2))
         (r1 (production-reward p1))
         (r2 (production-reward p2))
         (reward (or (and (numberp r1)
                          (numberp r2)
                          (max r1 r2))
                     (and (numberp r1) r1)
                     (and (numberp r2) r2)
                     r1 r2)))
    (setf (production-at new-p) at)
    ;;(setf (production-reward new-p) reward)
    (setf (production-u new-p) (car (no-output (sgp :nu))))))

(defvar *reward-value* 0)
(defvar *visited-points* nil)

(defun visit-point (point)
  (setf *visited-points* (cons point *visited-points*)))

(defun get-visited-points ()
  (reverse *visited-points*))

(defun clear-points ()
  (setf *visited-points* nil))

(defun set-reward-value (value)
  (setf *reward-value* value))