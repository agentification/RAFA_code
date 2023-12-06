

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(on c f)
(on d a)
(on e d)
(ontable f)
(ontable g)
(ontable h)
(on i b)
(clear c)
(clear e)
(clear h)
(clear i)
)
(:goal
(and
(on a i)
(on b h)
(on c g)
(on d f)
(on e b)
(on f a)
(on g d)
(on h c))
)
)


