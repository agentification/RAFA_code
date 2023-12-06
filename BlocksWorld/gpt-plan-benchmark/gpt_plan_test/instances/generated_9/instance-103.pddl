

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(ontable b)
(on c a)
(on d e)
(on e f)
(on f i)
(ontable g)
(on h g)
(ontable i)
(clear b)
(clear c)
(clear d)
)
(:goal
(and
(on a e)
(on d a)
(on e c)
(on g d)
(on h i)
(on i g))
)
)


