

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a i)
(ontable b)
(on c h)
(on d g)
(ontable e)
(on f a)
(on g b)
(on h e)
(on i c)
(clear d)
(clear f)
)
(:goal
(and
(on b g)
(on d f)
(on f h)
(on g i)
(on i e))
)
)


