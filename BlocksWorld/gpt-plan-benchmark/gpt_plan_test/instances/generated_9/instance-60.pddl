

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b f)
(on c e)
(ontable d)
(on e b)
(ontable f)
(on g a)
(ontable h)
(on i g)
(clear d)
(clear h)
(clear i)
)
(:goal
(and
(on a d)
(on b g)
(on c f)
(on d c)
(on e h)
(on f b)
(on i a))
)
)


