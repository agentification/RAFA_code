

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b g)
(ontable c)
(on d i)
(ontable e)
(ontable f)
(on g d)
(on h f)
(ontable i)
(clear a)
(clear c)
(clear e)
(clear h)
)
(:goal
(and
(on b d)
(on c b)
(on e h)
(on f e)
(on h a)
(on i c))
)
)


