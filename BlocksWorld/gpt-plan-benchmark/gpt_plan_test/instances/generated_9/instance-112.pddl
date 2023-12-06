

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(ontable c)
(on d i)
(on e c)
(ontable f)
(on g h)
(ontable h)
(on i b)
(clear a)
(clear d)
(clear e)
(clear f)
)
(:goal
(and
(on b f)
(on c g)
(on e b)
(on g a)
(on i h))
)
)


