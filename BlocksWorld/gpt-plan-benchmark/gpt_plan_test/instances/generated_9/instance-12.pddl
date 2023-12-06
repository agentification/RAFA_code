

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a i)
(on b c)
(on c e)
(on d b)
(on e g)
(on f d)
(on g a)
(on h f)
(ontable i)
(clear h)
)
(:goal
(and
(on a f)
(on b e)
(on e a)
(on f i)
(on g d)
(on h c))
)
)


