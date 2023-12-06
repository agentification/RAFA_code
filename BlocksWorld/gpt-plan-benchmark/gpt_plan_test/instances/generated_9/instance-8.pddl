

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c b)
(on d i)
(on e f)
(on f d)
(on g c)
(on h e)
(on i g)
(clear a)
(clear h)
)
(:goal
(and
(on a b)
(on b h)
(on c a)
(on d f)
(on e i)
(on f c)
(on i d))
)
)


