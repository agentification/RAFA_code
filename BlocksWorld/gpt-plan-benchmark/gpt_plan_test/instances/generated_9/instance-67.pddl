

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(on d e)
(on e c)
(on f g)
(on g i)
(on h a)
(on i h)
(clear b)
(clear f)
)
(:goal
(and
(on a b)
(on b c)
(on c h)
(on d i)
(on e a)
(on f e)
(on h d))
)
)


