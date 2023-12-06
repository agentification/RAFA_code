

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c b)
(on d h)
(on e g)
(on f e)
(ontable g)
(on h i)
(ontable i)
(clear a)
(clear c)
(clear d)
)
(:goal
(and
(on a h)
(on c f)
(on d i)
(on e c)
(on f a)
(on g d))
)
)


