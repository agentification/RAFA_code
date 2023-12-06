

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b c)
(on c a)
(ontable d)
(on e h)
(ontable f)
(on g f)
(on h d)
(on i e)
(clear b)
(clear g)
(clear i)
)
(:goal
(and
(on a i)
(on b e)
(on c f)
(on d h)
(on e g)
(on f b)
(on g d)
(on h a))
)
)


