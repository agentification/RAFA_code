

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(on b f)
(on c g)
(ontable d)
(ontable e)
(on f c)
(on g e)
(on h a)
(on i h)
(clear b)
(clear i)
)
(:goal
(and
(on a i)
(on c d)
(on d h)
(on e c)
(on f a)
(on g e)
(on i b))
)
)


