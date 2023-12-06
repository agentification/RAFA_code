

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(on d i)
(on e d)
(on f h)
(on g f)
(on h c)
(on i g)
(clear a)
(clear b)
)
(:goal
(and
(on a i)
(on b e)
(on c h)
(on d a)
(on g f)
(on i c))
)
)


