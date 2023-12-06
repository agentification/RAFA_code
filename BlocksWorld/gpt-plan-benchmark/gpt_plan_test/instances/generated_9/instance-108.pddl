

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(ontable b)
(on c g)
(on d b)
(on e f)
(on f c)
(ontable g)
(on h e)
(on i d)
(clear a)
(clear i)
)
(:goal
(and
(on a i)
(on b f)
(on c g)
(on e c)
(on g d))
)
)


