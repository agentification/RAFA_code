

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(ontable d)
(on e f)
(on f g)
(on g b)
(on h c)
(on i h)
(clear d)
(clear i)
)
(:goal
(and
(on a h)
(on c e)
(on d b)
(on e g)
(on f a)
(on h d))
)
)


