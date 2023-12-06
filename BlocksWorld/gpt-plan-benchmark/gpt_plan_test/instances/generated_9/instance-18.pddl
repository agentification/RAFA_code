

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(on c b)
(on d f)
(on e c)
(on f a)
(ontable g)
(ontable h)
(on i h)
(clear e)
(clear g)
(clear i)
)
(:goal
(and
(on a h)
(on c g)
(on d b)
(on e f)
(on g e)
(on i c))
)
)


