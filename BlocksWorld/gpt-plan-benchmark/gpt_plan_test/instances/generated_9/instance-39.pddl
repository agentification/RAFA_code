

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b e)
(on c f)
(ontable d)
(on e d)
(on f g)
(ontable g)
(on h i)
(on i b)
(clear a)
(clear c)
(clear h)
)
(:goal
(and
(on a b)
(on c d)
(on d a)
(on e h)
(on g c)
(on h g)
(on i e))
)
)


