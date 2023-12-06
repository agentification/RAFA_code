

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b h)
(on c g)
(on d a)
(on e d)
(on f e)
(on g b)
(on h f)
(ontable i)
(clear c)
(clear i)
)
(:goal
(and
(on a i)
(on c e)
(on d f)
(on f b)
(on g a)
(on h d)
(on i c))
)
)


