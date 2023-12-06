

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b e)
(on c b)
(ontable d)
(ontable e)
(on f h)
(on g f)
(on h d)
(ontable i)
(clear a)
(clear g)
(clear i)
)
(:goal
(and
(on a b)
(on c g)
(on e h)
(on f d)
(on g f))
)
)


