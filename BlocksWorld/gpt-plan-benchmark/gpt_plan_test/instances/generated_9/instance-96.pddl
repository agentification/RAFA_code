

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(on c f)
(ontable d)
(on e i)
(on f a)
(ontable g)
(on h d)
(on i h)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a f)
(on b c)
(on d e)
(on e a)
(on g d)
(on h g))
)
)


