

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b d)
(on c b)
(on d f)
(on e c)
(ontable f)
(ontable g)
(on h g)
(ontable i)
(clear a)
(clear h)
(clear i)
)
(:goal
(and
(on a b)
(on b g)
(on e i)
(on f e)
(on g h)
(on h c)
(on i d))
)
)


