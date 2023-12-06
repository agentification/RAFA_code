

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b e)
(on c f)
(ontable d)
(on e a)
(on f h)
(on g b)
(on h d)
(on i g)
(clear c)
(clear i)
)
(:goal
(and
(on b f)
(on c e)
(on d b)
(on e g)
(on f a)
(on h i)
(on i c))
)
)


