

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(ontable b)
(on c f)
(ontable d)
(on e g)
(on f e)
(on g h)
(ontable h)
(on i c)
(clear a)
(clear d)
(clear i)
)
(:goal
(and
(on a d)
(on b a)
(on c i)
(on e h)
(on f b)
(on g f)
(on i e))
)
)


