

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a i)
(ontable b)
(on c g)
(ontable d)
(on e a)
(ontable f)
(on g h)
(ontable h)
(on i b)
(clear c)
(clear d)
(clear e)
(clear f)
)
(:goal
(and
(on a d)
(on f b)
(on g e)
(on h g)
(on i a))
)
)


