

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a f)
(on b h)
(on c b)
(ontable d)
(on e g)
(on f e)
(on g d)
(on h a)
(on i c)
(clear i)
)
(:goal
(and
(on a g)
(on b e)
(on d b)
(on e i)
(on f d)
(on g h)
(on h c)
(on i a))
)
)


