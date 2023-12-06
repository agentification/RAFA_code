

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(ontable b)
(on c e)
(ontable d)
(ontable e)
(on f g)
(on g i)
(ontable h)
(on i a)
(clear b)
(clear c)
(clear f)
(clear h)
)
(:goal
(and
(on a d)
(on b c)
(on c e)
(on d b)
(on e i)
(on f h))
)
)


