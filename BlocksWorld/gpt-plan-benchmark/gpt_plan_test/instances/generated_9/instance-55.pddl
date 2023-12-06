

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c d)
(on d i)
(ontable e)
(on f c)
(ontable g)
(on h f)
(on i g)
(clear a)
(clear b)
(clear e)
(clear h)
)
(:goal
(and
(on a e)
(on b g)
(on c b)
(on d i)
(on f c)
(on h d))
)
)


