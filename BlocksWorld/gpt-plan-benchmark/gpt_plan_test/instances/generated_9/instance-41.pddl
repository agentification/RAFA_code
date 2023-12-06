

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(on c e)
(on d c)
(ontable e)
(ontable f)
(on g d)
(ontable h)
(on i b)
(clear a)
(clear f)
(clear h)
(clear i)
)
(:goal
(and
(on a d)
(on b h)
(on c f)
(on e b)
(on g i)
(on h g)
(on i c))
)
)


