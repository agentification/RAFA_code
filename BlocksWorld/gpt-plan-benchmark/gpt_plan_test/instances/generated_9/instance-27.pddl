

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b e)
(on c d)
(ontable d)
(ontable e)
(ontable f)
(on g b)
(ontable h)
(on i c)
(clear a)
(clear f)
(clear g)
(clear i)
)
(:goal
(and
(on d b)
(on e g)
(on f c)
(on g a)
(on h d))
)
)


