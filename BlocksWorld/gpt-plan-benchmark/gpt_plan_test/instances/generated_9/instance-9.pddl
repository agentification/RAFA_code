

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(ontable b)
(ontable c)
(ontable d)
(on e g)
(on f i)
(on g d)
(on h e)
(on i c)
(clear a)
(clear b)
(clear f)
)
(:goal
(and
(on a h)
(on c b)
(on e g)
(on f c)
(on g d))
)
)


