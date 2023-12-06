

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b e)
(on c d)
(on d i)
(on e f)
(on f a)
(on g h)
(ontable h)
(on i g)
(clear b)
(clear c)
)
(:goal
(and
(on b a)
(on e c)
(on f e)
(on g i)
(on i h))
)
)


