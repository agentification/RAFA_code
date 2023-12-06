

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(ontable b)
(on c b)
(on d f)
(on e h)
(ontable f)
(ontable g)
(ontable h)
(ontable i)
(clear a)
(clear d)
(clear e)
(clear g)
(clear i)
)
(:goal
(and
(on a e)
(on b h)
(on e i)
(on f a)
(on h f)
(on i c))
)
)


