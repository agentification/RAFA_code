

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b c)
(on c f)
(ontable d)
(on e g)
(on f a)
(ontable g)
(ontable h)
(on i h)
(clear b)
(clear d)
(clear e)
(clear i)
)
(:goal
(and
(on a d)
(on b c)
(on d g)
(on e i)
(on f b)
(on h f)
(on i h))
)
)


