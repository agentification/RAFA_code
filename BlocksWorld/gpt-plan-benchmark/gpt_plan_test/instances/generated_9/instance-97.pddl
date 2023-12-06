

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(on c b)
(on d h)
(ontable e)
(on f i)
(on g a)
(on h e)
(on i d)
(clear c)
(clear f)
)
(:goal
(and
(on a e)
(on c i)
(on e f)
(on g d)
(on h c)
(on i b))
)
)


