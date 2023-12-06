

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c g)
(on d f)
(ontable e)
(on f e)
(on g i)
(on h c)
(on i d)
(clear a)
(clear b)
(clear h)
)
(:goal
(and
(on a e)
(on b f)
(on c i)
(on e c)
(on f g)
(on g h)
(on h d)
(on i b))
)
)


