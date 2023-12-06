

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(on d h)
(ontable e)
(ontable f)
(ontable g)
(ontable h)
(on i c)
(clear a)
(clear e)
(clear f)
(clear g)
(clear i)
)
(:goal
(and
(on b f)
(on c i)
(on e c)
(on f d)
(on g a)
(on h e))
)
)


