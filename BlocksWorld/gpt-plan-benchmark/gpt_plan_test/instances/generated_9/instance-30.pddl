

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b a)
(on c g)
(ontable d)
(ontable e)
(on f h)
(ontable g)
(on h c)
(on i f)
(clear b)
(clear d)
(clear e)
(clear i)
)
(:goal
(and
(on a f)
(on c d)
(on f h)
(on g e)
(on h i)
(on i c))
)
)


